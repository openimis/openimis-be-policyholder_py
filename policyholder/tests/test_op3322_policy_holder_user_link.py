"""Who may attach which user to which policy holder (OP-3322).

A policy holder membership widens what the member reads and lets the portal
rights apply, so the link mutations check more than the right: the policy holder
must be in the caller's scope, and a caller may not attach themselves.
"""
from django.core.cache import cache
from django.test import TestCase, override_settings

from core.test_helpers import create_right_only_user, create_test_interactive_user
from location.models import Location
from location.test_helpers import create_basic_test_locations
from policyholder.gql.gql_mutations.create_mutations import CreatePolicyHolderUserMutation
from policyholder.gql.gql_mutations.replace_mutation import ReplacePolicyHolderUserMutation
from policyholder.gql.gql_mutations.update_mutations import UpdatePolicyHolderUserMutation
from policyholder.models import PolicyHolderUser
from policyholder.tests.helpers import create_test_policy_holder, create_test_policy_holder_user

LINK_PERMS = [
    "gql_mutation_create_policyholderuser_perms",
    "gql_mutation_update_policyholderuser_perms",
    "gql_mutation_replace_policyholderuser_perms",
]


@override_settings(ROW_SECURITY=True)
class PolicyHolderUserLinkTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_basic_test_locations()
        district_a = Location.objects.get(code="R1D1", validity_to__isnull=True)
        district_b = Location.objects.get(code="R2D1", validity_to__isnull=True)
        cls.ph_a = create_test_policy_holder(custom_props={"code": "OP3322-PHU-A", "locations": district_a})
        cls.ph_b = create_test_policy_holder(custom_props={"code": "OP3322-PHU-B", "locations": district_b})
        cls.caller = create_right_only_user("op3322phuc", LINK_PERMS, district_codes=["R1D1"])
        cls.member = create_test_interactive_user(username="op3322phum")

    def setUp(self):
        cache.clear()

    def _links(self, user, policy_holder):
        return PolicyHolderUser.objects.filter(user=user, policy_holder=policy_holder, is_deleted=False)

    def test_create_link_in_scope(self):
        errors = CreatePolicyHolderUserMutation.async_mutate(
            self.caller, user_id=self.member.id, policy_holder_id=self.ph_a.id)
        self.assertIsNone(errors)
        self.assertTrue(self._links(self.member, self.ph_a).exists())

    def test_create_link_out_of_scope_is_refused(self):
        errors = CreatePolicyHolderUserMutation.async_mutate(
            self.caller, user_id=self.member.id, policy_holder_id=self.ph_b.id)
        self.assertTrue(errors)
        self.assertFalse(self._links(self.member, self.ph_b).exists())

    def test_self_link_is_refused(self):
        errors = CreatePolicyHolderUserMutation.async_mutate(
            self.caller, user_id=self.caller.id, policy_holder_id=self.ph_a.id)
        self.assertTrue(errors)
        self.assertFalse(self._links(self.caller, self.ph_a).exists())

    def test_superuser_may_link_themselves(self):
        admin = create_test_interactive_user(username="op3322phuadm")
        self.assertTrue(admin.is_superuser)
        errors = CreatePolicyHolderUserMutation.async_mutate(
            admin, user_id=admin.id, policy_holder_id=self.ph_b.id)
        self.assertIsNone(errors)
        self.assertTrue(self._links(admin, self.ph_b).exists())

    def test_update_cannot_move_link_out_of_scope(self):
        link = create_test_policy_holder_user(user=self.member, policy_holder=self.ph_a)
        errors = UpdatePolicyHolderUserMutation.async_mutate(
            self.caller, id=link.id, user_id=self.member.id, policy_holder_id=self.ph_b.id)
        self.assertTrue(errors)
        link.refresh_from_db()
        self.assertEqual(link.policy_holder_id, self.ph_a.id)

    def test_update_cannot_retarget_link_to_caller(self):
        link = create_test_policy_holder_user(user=self.member, policy_holder=self.ph_a)
        errors = UpdatePolicyHolderUserMutation.async_mutate(
            self.caller, id=link.id, user_id=self.caller.id, policy_holder_id=self.ph_a.id)
        self.assertTrue(errors)
        link.refresh_from_db()
        self.assertEqual(link.user_id, self.member.id)

    def test_update_in_scope_still_works(self):
        link = create_test_policy_holder_user(user=self.member, policy_holder=self.ph_a)
        errors = UpdatePolicyHolderUserMutation.async_mutate(
            self.caller, id=link.id, user_id=self.member.id, policy_holder_id=self.ph_a.id,
            json_ext={"changed": True})
        self.assertIsNone(errors)
        link.refresh_from_db()
        self.assertEqual(link.json_ext, {"changed": True})

    def test_replace_cannot_move_link_out_of_scope(self):
        link = create_test_policy_holder_user(user=self.member, policy_holder=self.ph_a)
        errors = ReplacePolicyHolderUserMutation.async_mutate(
            self.caller, uuid=link.id, user_id=self.member.id, policy_holder_id=self.ph_b.id)
        self.assertTrue(errors)
        self.assertFalse(self._links(self.member, self.ph_b).exists())
