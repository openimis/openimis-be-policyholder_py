from core.gql.gql_mutations import ReplaceInputType
from core.gql.gql_mutations.base_mutation import BaseReplaceMutation, BaseHistoryModelReplaceMutationMixin
from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderContributionPlan, PolicyHolderUser


class ReplacePolicyHolderMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "PolicyHolderMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolder

    class Input(ReplaceInputType):
        pass


class ReplacePolicyHolderInsureeMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "PolicyHolderInsureeMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolderInsuree

    class Input(ReplaceInputType):
        pass


class ReplacePolicyHolderContributionPlanMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "PolicyHolderContributionPlanMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolderContributionPlan

    class Input(ReplaceInputType):
        pass


class ReplacePolicyHolderUserMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "PolicyHolderUserMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolderUser

    class Input(ReplaceInputType):
        pass