from django.apps import AppConfig


MODULE_NAME = "policyholder"


DEFAULT_CFG = {
    "gql_query_policyholder_perms": ["150101"],
    "gql_query_policyholder_admins_perms": [],
    "gql_query_policyholder_officers_perms": [],
    "gql_query_policyholderinsuree_perms": ["150201"],
    "gql_query_policyholderinsuree_admins_perms": [],
    "gql_query_policyholderinsuree_officers_perms": [],
    "gql_query_policyholderuser_perms": ["150301"],
    "gql_query_policyholderuser_admins_perms": [],
    "gql_query_policyholderuser_officers_perms": [],
    "gql_query_policyholdercontributionplanbundle_perms": ["150401"],
    "gql_query_policyholdercontributionplanbundle_admins_perms": [],
    "gql_query_policyholdercontributionplanbundle_officers_perms": [],
    "gql_mutation_create_policyholder_perms": ["150102"],
    "gql_mutation_update_policyholder_perms": ["150103"],
    "gql_mutation_delete_policyholder_perms": ["150104"],
    "gql_mutation_create_policyholderinsuree_perms": ["150202"],
    "gql_mutation_update_policyholderinsuree_perms": ["150203"],
    "gql_mutation_delete_policyholderinsuree_perms": ["150204"],
    "gql_mutation_replace_policyholderinsuree_perms": ["150206"],
    "gql_mutation_create_policyholderuser_perms": ["150302"],
    "gql_mutation_update_policyholderuser_perms": ["150303"],
    "gql_mutation_delete_policyholderuser_perms": ["150304"],
    "gql_mutation_replace_policyholderuser_perms": ["150306"],
    "gql_mutation_create_policyholdercontributionplan_perms": ["150402"],
    "gql_mutation_update_policyholdercontributionplan_perms": ["150403"],
    "gql_mutation_delete_policyholdercontributionplan_perms": ["150404"],
    "gql_mutation_replace_policyholdercontributionplan_perms": ["150406"],
}


class PolicyholderConfig(AppConfig):
    name = MODULE_NAME

    gql_query_policyholder_perms = []
    gql_query_policyholder_admins_perms = []
    gql_query_policyholder_officers_perms = []
    gql_query_policyholderinsuree_perms = []
    gql_query_policyholderinsuree_admins_perms = []
    gql_query_policyholderinsuree_officers_perms = []
    gql_query_policyholderuser_perms = []
    gql_query_policyholderuser_admins_perms = []
    gql_query_policyholderuser_officers_perms = []
    gql_query_policyholdercontributionplanbundle_perms = []
    gql_query_policyholdercontributionplanbundle_admins_perms = []
    gql_query_policyholdercontributionplanbundle_officers_perms = []
    gql_mutation_create_policyholder_perms = []
    gql_mutation_update_policyholder_perms = []
    gql_mutation_delete_policyholder_perms = []
    gql_mutation_create_policyholderinsuree_perms = []
    gql_mutation_update_policyholderinsuree_perms = []
    gql_mutation_delete_policyholderinsuree_perms = []
    gql_mutation_replace_policyholderinsuree_perms = []
    gql_mutation_create_policyholderuser_perms = []
    gql_mutation_update_policyholderuser_perms = []
    gql_mutation_delete_policyholderuser_perms = []
    gql_mutation_replace_policyholderuser_perms = []
    gql_mutation_create_policyholdercontributionplan_perms = []
    gql_mutation_update_policyholdercontributionplan_perms = []
    gql_mutation_delete_policyholdercontributionplan_perms = []
    gql_mutation_replace_policyholdercontributionplan_perms = []

    def _configure_permissions(self, cfg):
        PolicyholderConfig.gql_query_policyholder_perms = cfg[
            "gql_query_policyholder_perms"]
        PolicyholderConfig.gql_query_policyholder_admins_perms = cfg[
            "gql_query_policyholder_admins_perms"]
        PolicyholderConfig.gql_query_policyholder_officers_perms = cfg[
            "gql_query_policyholder_officers_perms"]

        PolicyholderConfig.gql_query_policyholderinsuree_perms = cfg[
            "gql_query_policyholderinsuree_perms"]
        PolicyholderConfig.gql_query_policyholderinsuree_admins_perms = cfg[
            "gql_query_policyholderinsuree_admins_perms"]
        PolicyholderConfig.gql_query_policyholderuser_officers_perms = cfg[
            "gql_query_policyholderuser_officers_perms"]

        PolicyholderConfig.gql_query_policyholderuser_perms = cfg[
            "gql_query_policyholderuser_perms"]
        PolicyholderConfig.gql_query_policyholderuser_admins_perms = cfg[
            "gql_query_policyholderuser_admins_perms"]
        PolicyholderConfig.gql_query_policyholderuser_officers_perms = cfg[
            "gql_query_policyholderuser_officers_perms"]

        PolicyholderConfig.gql_query_policyholdercontributionplanbundle_perms = cfg[
            "gql_query_policyholdercontributionplanbundle_perms"]
        PolicyholderConfig.gql_query_policyholdercontributionplanbundle_admins_perms = cfg[
            "gql_query_policyholdercontributionplanbundle_admins_perms"]
        PolicyholderConfig.gql_query_policyholdercontributionplanbundle_officers_perms = cfg[
            "gql_query_policyholdercontributionplanbundle_officers_perms"]

        PolicyholderConfig.gql_mutation_create_policyholder_perms = cfg[
            "gql_mutation_create_policyholder_perms"]
        PolicyholderConfig.gql_mutation_update_policyholder_perms = cfg[
            "gql_mutation_update_policyholder_perms"]
        PolicyholderConfig.gql_mutation_delete_policyholder_perms = cfg[
            "gql_mutation_delete_policyholder_perms"]

        PolicyholderConfig.gql_mutation_create_policyholderinsuree_perms = cfg[
            "gql_mutation_create_policyholderinsuree_perms"]
        PolicyholderConfig.gql_mutation_update_policyholderinsuree_perms = cfg[
            "gql_mutation_update_policyholderinsuree_perms"]
        PolicyholderConfig.gql_mutation_delete_policyholderinsuree_perms = cfg[
            "gql_mutation_delete_policyholderinsuree_perms"]
        PolicyholderConfig.gql_mutation_replace_policyholderinsuree_perms = cfg[
            "gql_mutation_replace_policyholderinsuree_perms"]

        PolicyholderConfig.gql_mutation_create_policyholderuser_perms = cfg[
            "gql_mutation_create_policyholderuser_perms"]
        PolicyholderConfig.gql_mutation_update_policyholderuser_perms = cfg[
            "gql_mutation_update_policyholderuser_perms"]
        PolicyholderConfig.gql_mutation_delete_policyholderuser_perms = cfg[
            "gql_mutation_delete_policyholderuser_perms"]
        PolicyholderConfig.gql_mutation_replace_policyholderuser_perms = cfg[
            "gql_mutation_replace_policyholderuser_perms"]

        PolicyholderConfig.gql_mutation_create_policyholdercontributionplan_perms = cfg[
            "gql_mutation_create_policyholdercontributionplan_perms"]
        PolicyholderConfig.gql_mutation_update_policyholdercontributionplan_perms = cfg[
            "gql_mutation_update_policyholdercontributionplan_perms"]
        PolicyholderConfig.gql_mutation_delete_policyholdercontributionplan_perms = cfg[
            "gql_mutation_delete_policyholdercontributionplan_perms"]
        PolicyholderConfig.gql_mutation_replace_policyholdercontributionplan_perms = cfg[
            "gql_mutation_replace_policyholdercontributionplan_perms"]

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_permissions(cfg)