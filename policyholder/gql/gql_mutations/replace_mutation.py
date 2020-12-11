from policyholder.gql.gql_mutations import PolicyHolderInsureeReplaceInputType, \
    PolicyHolderContributionPlanReplaceInputType, PolicyHolderUserReplaceInputType
from core.gql.gql_mutations.base_mutation import BaseReplaceMutation, BaseHistoryModelReplaceMutationMixin
from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderContributionPlan, PolicyHolderUser


class ReplacePolicyHolderInsureeMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "PolicyHolderInsureeMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolderInsuree

    class Input(PolicyHolderInsureeReplaceInputType):
        pass


class ReplacePolicyHolderContributionPlanMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "PolicyHolderContributionPlanMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolderContributionPlan

    class Input(PolicyHolderContributionPlanReplaceInputType):
        pass


class ReplacePolicyHolderUserMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "PolicyHolderUserMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolderUser

    class Input(PolicyHolderUserReplaceInputType):
        pass