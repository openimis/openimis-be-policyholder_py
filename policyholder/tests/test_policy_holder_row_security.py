"""Policy holders and their links stay in the user's districts or memberships (audit C7).

The back-office rights read what row security allows: the policy holders in the
user's districts, plus the ones the user is attached to. The portal rights read
only the policy holders the user is attached to.
"""

import json

from django.core.cache import cache
from django.test import override_settings

from core.models.openimis_graphql_test_case import openIMISGraphQLTestCase, BaseTestContext
from core.test_helpers import create_right_only_user
from location.models import Location
from location.test_helpers import create_basic_test_locations
from policyholder.gql.gql_mutations.delete_mutations import DeletePolicyHolderInsureeMutation
from policyholder.gql.gql_mutations.update_mutations import UpdatePolicyHolderInsureeMutation
from policyholder.models import PolicyHolderInsuree
from policyholder.tests.helpers import (
    create_test_policy_holder,
    create_test_policy_holder_contribution_plan,
    create_test_policy_holder_insuree,
    create_test_policy_holder_user,
)

CODES = {"C7-PH-A", "C7-PH-B"}
QUERIES = {
    "policyHolder": "query { policyHolder { edges { node { code } } } }",
    "policyHolderInsuree":
        "query { policyHolderInsuree { edges { node { policyHolder { code } } } } }",
    "policyHolderUser":
        "query { policyHolderUser { edges { node { policyHolder { code } } } } }",
    "policyHolderContributionPlanBundle":
        "query { policyHolderContributionPlanBundle { edges { node { policyHolder { code } } } } }",
}
BACK_OFFICE_PERMS = [
    "gql_query_policyholder_perms",
    "gql_query_policyholderinsuree_perms",
    "gql_query_policyholderuser_perms",
    "gql_query_policyholdercontributionplanbundle_perms",
]
PORTAL_PERMS = [
    "gql_query_policyholder_portal_perms",
    "gql_query_policyholderinsuree_portal_perms",
    "gql_query_policyholderuser_portal_perms",
    "gql_query_policyholdercontributionplanbundle_portal_perms",
]


class PolicyHolderScopeTestCase(openIMISGraphQLTestCase):
    """Two policy holders in two districts, and the users looking at them."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_basic_test_locations()
        district_a = Location.objects.get(code="R1D1", validity_to__isnull=True)
        district_b = Location.objects.get(code="R2D1", validity_to__isnull=True)
        ph_a = create_test_policy_holder(custom_props={"code": "C7-PH-A", "locations": district_a})
        ph_b = create_test_policy_holder(custom_props={"code": "C7-PH-B", "locations": district_b})
        cls.links = {}
        for key, ph in (("a", ph_a), ("b", ph_b)):
            cls.links[key] = create_test_policy_holder_insuree(policy_holder=ph)
            create_test_policy_holder_contribution_plan(policy_holder=ph)

        cls.staff_a = create_right_only_user("c7staffa", BACK_OFFICE_PERMS, district_codes=["R1D1"])
        cls.writer_a = create_right_only_user(
            "c7writera",
            [
                "gql_mutation_update_policyholderinsuree_perms",
                "gql_mutation_delete_policyholderinsuree_perms",
            ],
            district_codes=["R1D1"],
        )
        cls.staff_member = create_right_only_user("c7staffm", BACK_OFFICE_PERMS, district_codes=["R1D1"])
        # Portal accounts have no district: what they see comes from membership.
        cls.portal_a = create_right_only_user("c7portala", PORTAL_PERMS)
        cls.portal_none = create_right_only_user("c7portalnone", PORTAL_PERMS)
        cls.no_right = create_right_only_user("c7noright", [], district_codes=["R1D1"])
        create_test_policy_holder_user(user=cls.portal_a, policy_holder=ph_a)
        create_test_policy_holder_user(user=cls.staff_member, policy_holder=ph_b)
        cache.clear()

    def _gql(self, user, field):
        token = BaseTestContext(user=user).get_jwt()
        response = self.query(QUERIES[field], headers={"HTTP_AUTHORIZATION": f"Bearer {token}"})
        return json.loads(response.content)

    def _codes(self, user, field):
        content = self._gql(user, field)
        self.assertIsNone(content.get("errors"), field)
        nodes = [e["node"] for e in content["data"][field]["edges"]]
        codes = {n["code"] if "code" in n else n["policyHolder"]["code"] for n in nodes}
        return codes & CODES


@override_settings(ROW_SECURITY=True)
class PolicyHolderRowSecurityTests(PolicyHolderScopeTestCase):
    def test_portal_user_sees_only_own_policy_holder(self):
        for field in QUERIES:
            self.assertEqual(self._codes(self.portal_a, field), {"C7-PH-A"}, field)

    def test_portal_user_without_membership_sees_nothing(self):
        for field in QUERIES:
            self.assertEqual(self._codes(self.portal_none, field), set(), field)

    def test_back_office_sees_own_districts(self):
        for field in QUERIES:
            self.assertEqual(self._codes(self.staff_a, field), {"C7-PH-A"}, field)

    def test_membership_widens_back_office_rows(self):
        for field in QUERIES:
            self.assertEqual(self._codes(self.staff_member, field), CODES, field)

    def test_refused_without_right(self):
        for field in QUERIES:
            self.assertTrue(self._gql(self.no_right, field).get("errors"), field)


@override_settings(ROW_SECURITY=True)
class PolicyHolderWriteRowSecurityTests(PolicyHolderScopeTestCase):
    """Writes go through the shared mutation mixins, which look targets up scoped (H21)."""

    def _is_deleted(self, key):
        return PolicyHolderInsuree.objects.get(id=self.links[key].id).is_deleted

    def test_delete_refuses_foreign_link(self):
        errors = DeletePolicyHolderInsureeMutation.async_mutate(self.writer_a, uuids=[self.links["b"].id])
        self.assertTrue(errors)
        self.assertFalse(self._is_deleted("b"))

    def test_delete_own_link(self):
        errors = DeletePolicyHolderInsureeMutation.async_mutate(self.writer_a, uuids=[self.links["a"].id])
        self.assertIsNone(errors)
        self.assertTrue(self._is_deleted("a"))

    def test_update_refuses_foreign_link(self):
        errors = UpdatePolicyHolderInsureeMutation.async_mutate(
            self.writer_a, id=self.links["b"].id, json_ext={"h21": True}
        )
        self.assertTrue(errors)
        self.assertNotIn("h21", PolicyHolderInsuree.objects.get(id=self.links["b"].id).json_ext or {})
