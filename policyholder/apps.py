from django.apps import AppConfig

from core.rights_declaration import RightsDeclaration

MODULE_NAME = "policyholder"


# Rights, by entity then by action. Same structure as `core.apps.DJANGO_PERMS`.
#
# Four business entities, each with its back-office block (1501xx to 1504xx) and its
# *portal* variant (154xxx). The portal is not a mere relaxation of the back office: it
# is a distinct action, carried by a distinct identifier, whose scope is meant to be
# restricted to the policy holder the user is attached to through `PolicyHolderUser`.
# That is why `queryPortal` / `createPortal` / ... are declared as actions in their own
# right and not as aliases of `query` / `create`: a "portal" role must not be able to
# read everything, and merging the two would make that difference unsayable.
#
# `models.has_hybrid_phu_perms(user, ph, perms)` is the matching pattern on the check
# side: the right **and** membership of the policy holder. That is the shape every
# check of a `*Portal` action ought to take.
#
# The `queryAdmins` actions (xxxx05) are dormant declarations: no call site reads them.
# They stay declared because the identifier is already granted to deployed roles, and
# above all because the only alternative - not declaring the key - would make it hold
# `[]`, which `has_perms` grants to everybody.
DJANGO_PERMS = {
    "policyHolder": {
        "query": ("policyholder.view_policyholder", 150101),
        "create": ("policyholder.add_policyholder", 150102),
        "update": ("policyholder.change_policyholder", 150103),
        "delete": ("policyholder.delete_policyholder", 150104),
        # Dormant: slot 05 of the block (01 query, 02 create, 03 update, 04 delete,
        # 06 replace), nobody reads it.
        "queryAdmins": ("policyholder.view_policyholder_admins", 150105),
        # OFS-260: portal variant. Read by `Query.resolve_policy_holder`, the only
        # place in the module that actually restricts the result to the user's policy
        # holders.
        "queryPortal": ("policyholder.view_policyholder_portal", 154001),
        # Two rights carried by policyholder but governing the reading of another
        # module's data, seen from the policy holder's portal: payments (payment,
        # 1545xx) and insuree policies (insuree, 1549xx). They are declared here
        # because this module is the one that publishes them and because the catalogue
        # names them `policyholder.payment_portal` /
        # `policyholder.insuree_policy_portal`; their readers are
        # `policyholder/signals.py` and `contract/signals.py`, which OR them with the
        # owning module's back-office right.
        "queryPaymentPortal": ("policyholder.view_payment_portal", 154501),
        "queryInsureePolicyPortal": ("policyholder.view_insureepolicy_portal", 154901),
    },
    "policyHolderInsuree": {
        "query": ("policyholder.view_policyholderinsuree", 150201),
        "create": ("policyholder.add_policyholderinsuree", 150202),
        "update": ("policyholder.change_policyholderinsuree", 150203),
        "delete": ("policyholder.delete_policyholderinsuree", 150204),
        # Dormant: the block's free slot 05, no reader.
        "queryAdmins": ("policyholder.view_policyholderinsuree_admins", 150205),
        # A business action: `replace` closes the current row and opens a new one
        # (BaseHistoryModelReplaceMutationMixin). It is neither an update nor a delete,
        # and the catalogue gives it its own identifier.
        "replace": ("policyholder.replace_policyholderinsuree", 150206),
        # OFS-260: portal variant. The four portal mutations are dormant: no mutation
        # checks them today (see the conversion report).
        "queryPortal": ("policyholder.view_policyholderinsuree_portal", 154101),
        "createPortal": ("policyholder.add_policyholderinsuree_portal", 154102),
        "updatePortal": ("policyholder.change_policyholderinsuree_portal", 154103),
        "deletePortal": ("policyholder.delete_policyholderinsuree_portal", 154104),
        "replacePortal": ("policyholder.replace_policyholderinsuree_portal", 154106),
    },
    "policyHolderUser": {
        "query": ("policyholder.view_policyholderuser", 150301),
        "create": ("policyholder.add_policyholderuser", 150302),
        "update": ("policyholder.change_policyholderuser", 150303),
        "delete": ("policyholder.delete_policyholderuser", 150304),
        # Dormant: the block's free slot 05, no reader.
        "queryAdmins": ("policyholder.view_policyholderuser_admins", 150305),
        "replace": ("policyholder.replace_policyholderuser", 150306),
        # OFS-260: portal variant, block 1544xx. Dormant mutations.
        "queryPortal": ("policyholder.view_policyholderuser_portal", 154401),
        "createPortal": ("policyholder.add_policyholderuser_portal", 154402),
        "updatePortal": ("policyholder.change_policyholderuser_portal", 154403),
        "deletePortal": ("policyholder.delete_policyholderuser_portal", 154404),
        "replacePortal": ("policyholder.replace_policyholderuser_portal", 154406),
    },
    # The entity carries the name the config and the catalogue give it
    # (`policyholdercontributionplanbundle`), but the model behind it is
    # `PolicyHolderContributionPlan`: the canonical django names follow the model, not
    # the config key, otherwise they would match no django permission the day those are
    # really created.
    "policyHolderContributionPlanBundle": {
        "query": ("policyholder.view_policyholdercontributionplan", 150401),
        "create": ("policyholder.add_policyholdercontributionplan", 150402),
        "update": ("policyholder.change_policyholdercontributionplan", 150403),
        "delete": ("policyholder.delete_policyholdercontributionplan", 150404),
        # Dormant: the block's free slot 05, no reader.
        "queryAdmins": (
            "policyholder.view_policyholdercontributionplanbundle_admins",
            150405,
        ),
        "replace": ("policyholder.replace_policyholdercontributionplan", 150406),
        # OFS-260: portal variant, block 1546xx. Read only: the catalogue publishes no
        # portal mutation for this entity.
        "queryPortal": (
            "policyholder.view_policyholdercontributionplanbundle_portal",
            154601,
        ),
    },
}

_PERM_CFG = {
    "gql_query_policyholder_perms": ("policyHolder", "query"),
    "gql_query_policyholder_admins_perms": ("policyHolder", "queryAdmins"),
    "gql_mutation_create_policyholder_perms": ("policyHolder", "create"),
    "gql_mutation_update_policyholder_perms": ("policyHolder", "update"),
    "gql_mutation_delete_policyholder_perms": ("policyHolder", "delete"),
    "gql_query_policyholder_portal_perms": ("policyHolder", "queryPortal"),
    "gql_query_payment_portal_perms": ("policyHolder", "queryPaymentPortal"),
    "gql_query_insuree_policy_portal_perms": ("policyHolder", "queryInsureePolicyPortal"),

    "gql_query_policyholderinsuree_perms": ("policyHolderInsuree", "query"),
    "gql_query_policyholderinsuree_admins_perms": ("policyHolderInsuree", "queryAdmins"),
    "gql_mutation_create_policyholderinsuree_perms": ("policyHolderInsuree", "create"),
    "gql_mutation_update_policyholderinsuree_perms": ("policyHolderInsuree", "update"),
    "gql_mutation_delete_policyholderinsuree_perms": ("policyHolderInsuree", "delete"),
    "gql_mutation_replace_policyholderinsuree_perms": ("policyHolderInsuree", "replace"),
    "gql_query_policyholderinsuree_portal_perms": ("policyHolderInsuree", "queryPortal"),
    "gql_mutation_create_policyholderinsuree_portal_perms": ("policyHolderInsuree", "createPortal"),
    "gql_mutation_update_policyholderinsuree_portal_perms": ("policyHolderInsuree", "updatePortal"),
    "gql_mutation_delete_policyholderinsuree_portal_perms": ("policyHolderInsuree", "deletePortal"),
    "gql_mutation_replace_policyholderinsuree_portal_perms": ("policyHolderInsuree", "replacePortal"),

    "gql_query_policyholderuser_perms": ("policyHolderUser", "query"),
    "gql_query_policyholderuser_admins_perms": ("policyHolderUser", "queryAdmins"),
    "gql_mutation_create_policyholderuser_perms": ("policyHolderUser", "create"),
    "gql_mutation_update_policyholderuser_perms": ("policyHolderUser", "update"),
    "gql_mutation_delete_policyholderuser_perms": ("policyHolderUser", "delete"),
    "gql_mutation_replace_policyholderuser_perms": ("policyHolderUser", "replace"),
    "gql_query_policyholderuser_portal_perms": ("policyHolderUser", "queryPortal"),
    "gql_mutation_create_policyholderuser_portal_perms": ("policyHolderUser", "createPortal"),
    "gql_mutation_update_policyholderuser_portal_perms": ("policyHolderUser", "updatePortal"),
    "gql_mutation_delete_policyholderuser_portal_perms": ("policyHolderUser", "deletePortal"),
    "gql_mutation_replace_policyholderuser_portal_perms": ("policyHolderUser", "replacePortal"),

    "gql_query_policyholdercontributionplanbundle_perms": ("policyHolderContributionPlanBundle", "query"),
    "gql_query_policyholdercontributionplanbundle_admins_perms": ("policyHolderContributionPlanBundle", "queryAdmins"),
    "gql_mutation_create_policyholdercontributionplan_perms": ("policyHolderContributionPlanBundle", "create"),
    "gql_mutation_update_policyholdercontributionplan_perms": ("policyHolderContributionPlanBundle", "update"),
    "gql_mutation_delete_policyholdercontributionplan_perms": ("policyHolderContributionPlanBundle", "delete"),
    "gql_mutation_replace_policyholdercontributionplan_perms": ("policyHolderContributionPlanBundle", "replace"),
    "gql_query_policyholdercontributionplanbundle_portal_perms": ("policyHolderContributionPlanBundle", "queryPortal"),
}

RIGHTS = RightsDeclaration(MODULE_NAME, DJANGO_PERMS, _PERM_CFG)

perms = RIGHTS.perms
django_perms = RIGHTS.django_perm_names
configured_perms = RIGHTS.configured
require = RIGHTS.require


DEFAULT_CFG = {
    "policyholder_legal_form": [
        {
            "code": "1",
            "display": "Personal Company",
        },
        {
            "code": "2",
            "display": "Limited Risk Company",
        },
        {
            "code": "3",
            "display": "Association",
        },
        {
            "code": "4",
            "display": "Government",
        },
        {
            "code": "5",
            "display": "Union",
        },
    ],
    "policyholder_activity": [
        {
            "code": "1",
            "display": "Retail",
        },
        {
            "code": "2",
            "display": "Industry",
        },
        {
            "code": "3",
            "display": "Building",
        },
        {
            "code": "4",
            "display": "Sailing",
        },
        {
            "code": "5",
            "display": "Services",
        },
    ]
}


class PolicyholderConfig(AppConfig):
    name = MODULE_NAME

    # Rights: constants derived from DJANGO_PERMS, no longer overridable. They go
    # neither through DEFAULT_CFG nor through ready():
    # `ModuleConfiguration.get_or_default` now ignores any `_perms` key stored in the
    # database.
    gql_query_policyholder_perms = RIGHTS.perms("policyHolder", "query")
    gql_query_policyholder_admins_perms = RIGHTS.perms("policyHolder", "queryAdmins")
    gql_query_policyholderinsuree_perms = RIGHTS.perms("policyHolderInsuree", "query")
    gql_query_policyholderinsuree_admins_perms = RIGHTS.perms("policyHolderInsuree", "queryAdmins")
    gql_query_policyholderuser_perms = RIGHTS.perms("policyHolderUser", "query")
    gql_query_policyholderuser_admins_perms = RIGHTS.perms("policyHolderUser", "queryAdmins")
    gql_query_policyholdercontributionplanbundle_perms = RIGHTS.perms("policyHolderContributionPlanBundle", "query")
    gql_query_policyholdercontributionplanbundle_admins_perms = RIGHTS.perms(
        "policyHolderContributionPlanBundle", "queryAdmins"
    )
    gql_mutation_create_policyholder_perms = RIGHTS.perms("policyHolder", "create")
    gql_mutation_update_policyholder_perms = RIGHTS.perms("policyHolder", "update")
    gql_mutation_delete_policyholder_perms = RIGHTS.perms("policyHolder", "delete")
    gql_mutation_create_policyholderinsuree_perms = RIGHTS.perms("policyHolderInsuree", "create")
    gql_mutation_update_policyholderinsuree_perms = RIGHTS.perms("policyHolderInsuree", "update")
    gql_mutation_delete_policyholderinsuree_perms = RIGHTS.perms("policyHolderInsuree", "delete")
    gql_mutation_replace_policyholderinsuree_perms = RIGHTS.perms("policyHolderInsuree", "replace")
    gql_mutation_create_policyholderuser_perms = RIGHTS.perms("policyHolderUser", "create")
    gql_mutation_update_policyholderuser_perms = RIGHTS.perms("policyHolderUser", "update")
    gql_mutation_delete_policyholderuser_perms = RIGHTS.perms("policyHolderUser", "delete")
    gql_mutation_replace_policyholderuser_perms = RIGHTS.perms("policyHolderUser", "replace")
    gql_mutation_create_policyholdercontributionplan_perms = RIGHTS.perms(
        "policyHolderContributionPlanBundle", "create"
    )
    gql_mutation_update_policyholdercontributionplan_perms = RIGHTS.perms(
        "policyHolderContributionPlanBundle", "update"
    )
    gql_mutation_delete_policyholdercontributionplan_perms = RIGHTS.perms(
        "policyHolderContributionPlanBundle", "delete"
    )
    gql_mutation_replace_policyholdercontributionplan_perms = RIGHTS.perms(
        "policyHolderContributionPlanBundle", "replace"
    )
    # OFS-260: Support the policyholder portal perms on Policyholder
    gql_query_policyholder_portal_perms = RIGHTS.perms("policyHolder", "queryPortal")
    gql_query_policyholderinsuree_portal_perms = RIGHTS.perms("policyHolderInsuree", "queryPortal")
    gql_query_policyholdercontributionplanbundle_portal_perms = RIGHTS.perms(
        "policyHolderContributionPlanBundle", "queryPortal"
    )
    gql_query_policyholderuser_portal_perms = RIGHTS.perms("policyHolderUser", "queryPortal")
    # Portal rights over other modules' objects, read by policyholder/signals.py and
    # contract/signals.py.
    gql_query_payment_portal_perms = RIGHTS.perms("policyHolder", "queryPaymentPortal")
    gql_query_insuree_policy_portal_perms = RIGHTS.perms("policyHolder", "queryInsureePolicyPortal")
    gql_mutation_create_policyholderinsuree_portal_perms = RIGHTS.perms("policyHolderInsuree", "createPortal")
    gql_mutation_update_policyholderinsuree_portal_perms = RIGHTS.perms("policyHolderInsuree", "updatePortal")
    gql_mutation_delete_policyholderinsuree_portal_perms = RIGHTS.perms("policyHolderInsuree", "deletePortal")
    gql_mutation_replace_policyholderinsuree_portal_perms = RIGHTS.perms("policyHolderInsuree", "replacePortal")
    gql_mutation_create_policyholderuser_portal_perms = RIGHTS.perms("policyHolderUser", "createPortal")
    gql_mutation_update_policyholderuser_portal_perms = RIGHTS.perms("policyHolderUser", "updatePortal")
    gql_mutation_delete_policyholderuser_portal_perms = RIGHTS.perms("policyHolderUser", "deletePortal")
    gql_mutation_replace_policyholderuser_portal_perms = RIGHTS.perms("policyHolderUser", "replacePortal")

    policyholder_legal_form = []
    policyholder_activity = []

    def __load_config(self, cfg):
        for field in cfg:
            if hasattr(PolicyholderConfig, field):
                setattr(PolicyholderConfig, field, cfg[field])

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self.__load_config(cfg)
