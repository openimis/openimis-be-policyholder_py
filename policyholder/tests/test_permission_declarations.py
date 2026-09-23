"""
Guard rails on policyholder's rights declaration.

Same structure as `claim`, `product` and `contribution_plan`: `DJANGO_PERMS` by entity
then by action, `_PERM_CFG` deriving the config keys from it, and a `get_rights` on
each main model which is only an access point.

What is locked down here is the entity/action pair, not only the values:
  * an identifier in one place only (DJANGO_PERMS), hence no drift between the
    DEFAULT_CFG and the check;
  * a config key with no class attribute is never loaded by `__load_config` and
    reading it raises AttributeError - the right becomes unenforceable;
  * `has_perms([])` returns True, so an empty list grants to everybody.

What is particular to this module: every entity carries a *portal* variant (154xxx)
alongside its back-office variant (1501xx to 1504xx). These are distinct actions, with
distinct identifiers, and the test below checks that no identifier is shared between
the two - conflating them would amount to giving the portal the back office's scope.
"""

import json
import os

from django.test import TestCase

from policyholder.apps import (
    DJANGO_PERMS,
    PolicyholderConfig,
    _PERM_CFG,
    configured_perms,
    django_perms,
    perms,
)
from policyholder.models import (
    PolicyHolder,
    PolicyHolderContributionPlan,
    PolicyHolderInsuree,
    PolicyHolderUser,
)

# The identifiers as deployed. Changing one is incompatible with the existing roles:
# this test has to be updated *and* the new right granted.
EXPECTED_RIGHTS = {
    # policyHolder - back-office
    "gql_query_policyholder_perms": ["150101"],
    "gql_mutation_create_policyholder_perms": ["150102"],
    "gql_mutation_update_policyholder_perms": ["150103"],
    "gql_mutation_delete_policyholder_perms": ["150104"],
    "gql_query_policyholder_admins_perms": ["150105"],
    # policyHolder - portail
    "gql_query_policyholder_portal_perms": ["154001"],
    "gql_query_payment_portal_perms": ["154501"],
    "gql_query_insuree_policy_portal_perms": ["154901"],
    # policyHolderInsuree - back-office
    "gql_query_policyholderinsuree_perms": ["150201"],
    "gql_mutation_create_policyholderinsuree_perms": ["150202"],
    "gql_mutation_update_policyholderinsuree_perms": ["150203"],
    "gql_mutation_delete_policyholderinsuree_perms": ["150204"],
    "gql_query_policyholderinsuree_admins_perms": ["150205"],
    "gql_mutation_replace_policyholderinsuree_perms": ["150206"],
    # policyHolderInsuree - portail
    "gql_query_policyholderinsuree_portal_perms": ["154101"],
    "gql_mutation_create_policyholderinsuree_portal_perms": ["154102"],
    "gql_mutation_update_policyholderinsuree_portal_perms": ["154103"],
    "gql_mutation_delete_policyholderinsuree_portal_perms": ["154104"],
    "gql_mutation_replace_policyholderinsuree_portal_perms": ["154106"],
    # policyHolderUser - back-office
    "gql_query_policyholderuser_perms": ["150301"],
    "gql_mutation_create_policyholderuser_perms": ["150302"],
    "gql_mutation_update_policyholderuser_perms": ["150303"],
    "gql_mutation_delete_policyholderuser_perms": ["150304"],
    "gql_query_policyholderuser_admins_perms": ["150305"],
    "gql_mutation_replace_policyholderuser_perms": ["150306"],
    # policyHolderUser - portail
    "gql_query_policyholderuser_portal_perms": ["154401"],
    "gql_mutation_create_policyholderuser_portal_perms": ["154402"],
    "gql_mutation_update_policyholderuser_portal_perms": ["154403"],
    "gql_mutation_delete_policyholderuser_portal_perms": ["154404"],
    "gql_mutation_replace_policyholderuser_portal_perms": ["154406"],
    # policyHolderContributionPlanBundle - back-office
    "gql_query_policyholdercontributionplanbundle_perms": ["150401"],
    "gql_mutation_create_policyholdercontributionplan_perms": ["150402"],
    "gql_mutation_update_policyholdercontributionplan_perms": ["150403"],
    "gql_mutation_delete_policyholdercontributionplan_perms": ["150404"],
    "gql_query_policyholdercontributionplanbundle_admins_perms": ["150405"],
    "gql_mutation_replace_policyholdercontributionplan_perms": ["150406"],
    # policyHolderContributionPlanBundle - portail
    "gql_query_policyholdercontributionplanbundle_portal_perms": ["154601"],
}

# The `permissions_map.json` entries that carry these identifiers. The historical name
# in the openIMIS catalogue is not the django name declared in DJANGO_PERMS: what has to
# stay stable is the integer.
EXPECTED_MAP_ENTRIES = {
    "policyholder.policyholder": "150101",
    "policyholder.create_policyholder": "150102",
    "policyholder.update_policyholder": "150103",
    "policyholder.delete_policyholder": "150104",
    "policyholder.policyholder_admins": "150105",
    "policyholder.policyholderinsuree": "150201",
    "policyholder.create_policyholderinsuree": "150202",
    "policyholder.update_policyholderinsuree": "150203",
    "policyholder.delete_policyholderinsuree": "150204",
    "policyholder.policyholderinsuree_admins": "150205",
    "policyholder.replace_policyholderinsuree": "150206",
    "policyholder.policyholderuser": "150301",
    "policyholder.create_policyholderuser": "150302",
    "policyholder.update_policyholderuser": "150303",
    "policyholder.delete_policyholderuser": "150304",
    "policyholder.policyholderuser_admins": "150305",
    "policyholder.replace_policyholderuser": "150306",
    "policyholder.policyholdercontributionplanbundle": "150401",
    "policyholder.create_policyholdercontributionplan": "150402",
    "policyholder.update_policyholdercontributionplan": "150403",
    "policyholder.delete_policyholdercontributionplan": "150404",
    "policyholder.policyholdercontributionplanbundle_admins": "150405",
    "policyholder.replace_policyholdercontributionplan": "150406",
    "policyholder.policyholder_portal": "154001",
    "policyholder.policyholderinsuree_portal": "154101",
    "policyholder.create_policyholderinsuree_portal": "154102",
    "policyholder.update_policyholderinsuree_portal": "154103",
    "policyholder.delete_policyholderinsuree_portal": "154104",
    "policyholder.replace_policyholderinsuree_portal": "154106",
    "policyholder.policyholderuser_portal": "154401",
    "policyholder.create_policyholderuser_portal": "154402",
    "policyholder.update_policyholderuser_portal": "154403",
    "policyholder.delete_policyholderuser_portal": "154404",
    "policyholder.replace_policyholderuser_portal": "154406",
    "policyholder.payment_portal": "154501",
    "policyholder.policyholdercontributionplanbundle_portal": "154601",
    "policyholder.insuree_policy_portal": "154901",
}

# Keys declared but which no call site reads. Kept because the identifiers are already
# granted to deployed roles; listed here so that adding a reader, or removing the key,
# is a visible decision.
#
# The four `*_admins_perms` have been dormant from the start. The eight portal
# mutations are so for a different reason: the matching mutations do exist
# (create/update/delete/replace of PolicyHolderInsuree and PolicyHolderUser) but only
# check the back-office right. That is an authorisation hole, reported and not fixed
# here: fixing it is another batch of work.
DORMANT_KEYS = {
    "gql_query_policyholder_admins_perms",
    "gql_query_policyholderinsuree_admins_perms",
    "gql_query_policyholderuser_admins_perms",
    "gql_query_policyholdercontributionplanbundle_admins_perms",
    "gql_mutation_create_policyholderinsuree_portal_perms",
    "gql_mutation_update_policyholderinsuree_portal_perms",
    "gql_mutation_delete_policyholderinsuree_portal_perms",
    "gql_mutation_replace_policyholderinsuree_portal_perms",
    "gql_mutation_create_policyholderuser_portal_perms",
    "gql_mutation_update_policyholderuser_portal_perms",
    "gql_mutation_delete_policyholderuser_portal_perms",
    "gql_mutation_replace_policyholderuser_portal_perms",
}

MODEL_BY_ENTITY = {
    "policyHolder": PolicyHolder,
    "policyHolderInsuree": PolicyHolderInsuree,
    "policyHolderUser": PolicyHolderUser,
    "policyHolderContributionPlanBundle": PolicyHolderContributionPlan,
}

# The three sub-resources and the foreign key that owns them.
SUB_RESOURCES = {
    PolicyHolderInsuree: "policy_holder",
    PolicyHolderUser: "policy_holder",
    PolicyHolderContributionPlan: "policy_holder",
}


def _permissions_map():
    """`permissions_map.json` lives in the assembly, not in the package."""
    from django.conf import settings

    candidates = [
        os.path.join(str(settings.BASE_DIR), "permissions_map.json"),
        os.path.join(os.path.dirname(str(settings.BASE_DIR)), "permissions_map.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path) as handle:
                return json.load(handle)
    return None


class PolicyHolderPermissionDeclarationTestCase(TestCase):
    def test_right_ids_unchanged(self):
        self.assertEqual(
            {key: getattr(PolicyholderConfig, key) for key in EXPECTED_RIGHTS},
            EXPECTED_RIGHTS,
        )

    def test_every_config_key_is_pinned(self):
        """A key added without an expected identifier would otherwise slip by."""
        self.assertEqual(set(_PERM_CFG), set(EXPECTED_RIGHTS))

    def test_perm_cfg_covers_every_declared_action(self):
        declared = {
            (entity, action)
            for entity, actions in DJANGO_PERMS.items()
            for action in actions
        }
        self.assertEqual(set(_PERM_CFG.values()), declared)

    def test_perm_cfg_matches_config_attributes(self):
        """`__load_config` ignores the keys with no class attribute."""
        missing = [key for key in _PERM_CFG if not hasattr(PolicyholderConfig, key)]
        self.assertEqual(missing, [])

    def test_no_right_list_is_empty(self):
        empty = [key for key in _PERM_CFG if not getattr(PolicyholderConfig, key)]
        self.assertEqual(empty, [])

    def test_attributes_carry_the_declared_right(self):
        for key, (entity, action) in _PERM_CFG.items():
            with self.subTest(key=key):
                self.assertEqual(
                    getattr(PolicyholderConfig, key), perms(entity, action)
                )

    def test_no_right_id_is_shared(self):
        """
        Four entities, two variants each, and no identifier in common: the portal is
        not an alias of the back office.
        """
        seen = {}
        for entity, actions in DJANGO_PERMS.items():
            for action, (_, right_id) in actions.items():
                seen.setdefault(right_id, []).append(f"{entity}.{action}")
        shared = {right: who for right, who in seen.items() if len(who) > 1}
        self.assertEqual(shared, {})

    def test_portal_actions_are_distinct_from_their_back_office_twin(self):
        """
        A portal right is meant to open the action only over the user's own policy
        holder. If it shared the back-office right's identifier, that restriction would
        become unsayable.
        """
        for entity, actions in DJANGO_PERMS.items():
            for action in actions:
                if not action.endswith("Portal"):
                    continue
                twin = action[: -len("Portal")]
                if twin not in actions:
                    continue
                with self.subTest(entity=entity, action=action):
                    self.assertNotEqual(
                        actions[action][1], actions[twin][1],
                        f"{entity}.{action} reprend l'identifiant de {twin}",
                    )

    def test_django_permission_names_are_unique(self):
        seen = {}
        for entity, actions in DJANGO_PERMS.items():
            for action, (name, _) in actions.items():
                seen.setdefault(name, []).append(f"{entity}.{action}")
        shared = {name: who for name, who in seen.items() if len(who) > 1}
        self.assertEqual(shared, {})

    def test_unknown_entity_or_action_raises(self):
        with self.assertRaises(KeyError):
            perms("nosuchentity", "query")
        with self.assertRaises(KeyError):
            perms("policyHolder", "nosuchaction")
        with self.assertRaises(KeyError):
            django_perms("policyHolderUser", "nosuchaction")

    def test_dormant_keys_are_still_declared(self):
        """
        Nobody reads them; they must carry their identifier all the same, and not [],
        otherwise the day a check does read them it will grant the action to everybody.
        """
        for key in DORMANT_KEYS:
            with self.subTest(key=key):
                self.assertIn(key, _PERM_CFG)
                self.assertEqual(getattr(PolicyholderConfig, key), EXPECTED_RIGHTS[key])

    def test_ids_match_permissions_map(self):
        mapping = _permissions_map()
        if mapping is None:
            self.skipTest("permissions_map.json absent de cet assemblage")
        actual = {name: mapping.get(name) for name in EXPECTED_MAP_ENTRIES}
        self.assertEqual(actual, EXPECTED_MAP_ENTRIES)

    # --- the access point through the model -------------------------------
    def test_each_model_exposes_every_action_of_its_entity(self):
        for entity, model in MODEL_BY_ENTITY.items():
            for action in DJANGO_PERMS[entity]:
                with self.subTest(entity=entity, action=action):
                    self.assertEqual(
                        model.get_rights(action), configured_perms(entity, action)
                    )
                    self.assertTrue(model.get_rights(action))

    def test_model_returns_none_for_an_undeclared_action(self):
        """None means "no rule": the caller must fail closed."""
        self.assertIsNone(PolicyHolder.get_rights("nosuchaction"))

    def test_model_reads_the_configured_value_not_the_declared_default(self):
        original = PolicyholderConfig.gql_query_policyholder_perms
        try:
            PolicyholderConfig.gql_query_policyholder_perms = ["999999"]
            self.assertEqual(PolicyHolder.get_rights("query"), ["999999"])
            self.assertEqual(perms("policyHolder", "query"), ["150101"])
        finally:
            PolicyholderConfig.gql_query_policyholder_perms = original

    # --- the sub-resources ------------------------------------------------
    def test_sub_resources_declare_the_owning_foreign_key(self):
        """
        The three sub-resources have several FKs and only one is the owner:
        `policy_holder`. The others (insuree, contribution_plan_bundle, last_policy,
        user) denote shared objects the row references.
        """
        from core.rights_scope import scope_parent_of

        for model, field in SUB_RESOURCES.items():
            with self.subTest(model=model.__name__):
                self.assertEqual(model.scope_parent, field)
                self.assertIs(scope_parent_of(model), PolicyHolder)

    def test_sub_resources_keep_their_own_rights(self):
        """
        Unlike a pure sub-resource (ContractDetails), these have their own block of
        identifiers: `scope_parent` is only a fallback for an action they do not
        declare.
        """
        from core.rights_scope import model_rights

        for model in SUB_RESOURCES:
            with self.subTest(model=model.__name__):
                self.assertNotEqual(
                    model.get_rights("query"), PolicyHolder.get_rights("query")
                )
                # une action que seule l'entite parente declare remonte au parent
                self.assertEqual(
                    model_rights(model, "queryPaymentPortal"),
                    PolicyHolder.get_rights("queryPaymentPortal"),
                )
