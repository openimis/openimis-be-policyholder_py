"""The "Show deleted" filter on policy holders and their insurees, users and bundles.

The list resolvers decide the soft-delete scope through append_validity_filter:
deleted rows are hidden by default, returned with isDeleted: true, and a lookup
by id finds the record whatever its state (OP-3256). A model get_queryset that
forces is_deleted=False on top of that turns isDeleted: true into
is_deleted=True AND is_deleted=False, an empty list (follow-up of OP-3180).
"""
import base64
from uuid import UUID

from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from core.models.openimis_graphql_test_case import BaseTestContext
from core.test_helpers import create_test_interactive_user
from policyholder import schema as policyholder_schema
from policyholder.gql.gql_mutations.replace_mutation import ReplacePolicyHolderUserMutation
from policyholder.gql.gql_mutations.update_mutations import (
    UpdatePolicyHolderInsureeMutation,
    UpdatePolicyHolderMutation,
    UpdatePolicyHolderUserMutation,
)
from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderUser
from policyholder.tests.helpers import (
    create_test_policy_holder,
    create_test_policy_holder_contribution_plan,
    create_test_policy_holder_insuree,
    create_test_policy_holder_user,
)


class ShowDeletedTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_test_interactive_user(username="phShowDeleted")
        cls.ph = create_test_policy_holder(custom_props={"code": "SD-PH-LIVE"})
        cls.deleted_ph = create_test_policy_holder(custom_props={"code": "SD-PH-DEL"})
        cls.rows = {
            "policyHolder": (cls.ph, cls.deleted_ph),
            "policyHolderInsuree": (
                create_test_policy_holder_insuree(policy_holder=cls.ph),
                create_test_policy_holder_insuree(policy_holder=cls.ph),
            ),
            "policyHolderUser": (
                create_test_policy_holder_user(user=cls.user, policy_holder=cls.ph),
                create_test_policy_holder_user(user=cls.user, policy_holder=cls.ph),
            ),
            "policyHolderContributionPlanBundle": (
                create_test_policy_holder_contribution_plan(policy_holder=cls.ph),
                create_test_policy_holder_contribution_plan(policy_holder=cls.ph),
            ),
        }
        for _live, deleted in cls.rows.values():
            deleted.delete(username=cls.user.username)

    def setUp(self):
        self.client_gql = Client(Schema(query=policyholder_schema.Query))
        self.context = BaseTestContext(self.user).get_request()

    def _ids(self, field, args):
        args = f"({args})" if args else ""
        query = f"{{ {field}{args} {{ edges {{ node {{ id }} }} }} }}"
        result = self.client_gql.execute(query, context=self.context)
        self.assertIsNone(result.get("errors"), result.get("errors"))
        return {
            UUID(base64.b64decode(edge["node"]["id"]).decode("utf-8").split(":")[1])
            for edge in result["data"][field]["edges"]
        }

    def _check(self, field):
        live, deleted = self.rows[field]
        # The children are listed under the live policy holder, as the UI does.
        scope = "" if field == "policyHolder" else f'policyHolder_Id: "{self.ph.id}"'
        sep = ", " if scope else ""

        shown = self._ids(field, f"isDeleted: true{sep}{scope}")
        self.assertIn(deleted.id, shown, "isDeleted: true must return the soft-deleted row")
        self.assertNotIn(live.id, shown, "isDeleted: true must not return live rows")

        default = self._ids(field, scope)
        self.assertIn(live.id, default, "the default list must return live rows")
        self.assertNotIn(deleted.id, default, "the default list must hide soft-deleted rows")

        by_id = self._ids(field, f'id: "{deleted.id}"')
        self.assertEqual(by_id, {deleted.id}, "a lookup by id must find a soft-deleted row (OP-3256)")

    def test_policy_holder_show_deleted(self):
        self._check("policyHolder")

    def test_policy_holder_insuree_show_deleted(self):
        self._check("policyHolderInsuree")

    def test_policy_holder_user_show_deleted(self):
        self._check("policyHolderUser")

    def test_policy_holder_contribution_plan_bundle_show_deleted(self):
        self._check("policyHolderContributionPlanBundle")

    # Mutations look their target up through get_queryset (core target_queryset).
    # Showing deleted rows must not make them writable.

    def test_update_refuses_deleted_policy_holder(self):
        errors = UpdatePolicyHolderMutation.async_mutate(
            self.user, id=self.deleted_ph.id, trade_name="changed")
        self.assertTrue(errors)
        self.assertNotEqual(PolicyHolder.objects.get(id=self.deleted_ph.id).trade_name, "changed")

    def test_update_refuses_deleted_policy_holder_insuree(self):
        deleted = self.rows["policyHolderInsuree"][1]
        errors = UpdatePolicyHolderInsureeMutation.async_mutate(
            self.user, id=deleted.id, json_ext={"changed": True})
        self.assertTrue(errors)
        self.assertNotIn("changed", PolicyHolderInsuree.objects.get(id=deleted.id).json_ext or {})

    def test_update_refuses_deleted_policy_holder_user(self):
        deleted = self.rows["policyHolderUser"][1]
        errors = UpdatePolicyHolderUserMutation.async_mutate(
            self.user, id=deleted.id, json_ext={"changed": True})
        self.assertTrue(errors)
        self.assertNotIn("changed", PolicyHolderUser.objects.get(id=deleted.id).json_ext or {})

    def test_replace_refuses_deleted_policy_holder_user(self):
        deleted = self.rows["policyHolderUser"][1]
        errors = ReplacePolicyHolderUserMutation.async_mutate(
            self.user, uuid=deleted.id, user_id=self.user.id, policy_holder_id=self.ph.id)
        self.assertTrue(errors)
        self.assertIsNone(PolicyHolderUser.objects.get(id=deleted.id).replacement_uuid)
