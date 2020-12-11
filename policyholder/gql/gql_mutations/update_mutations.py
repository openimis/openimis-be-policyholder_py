from core.gql.gql_mutations.base_mutation import BaseMutation, BaseHistoryModelUpdateMutationMixin
from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderContributionPlan, PolicyHolderUser
from policyholder.gql.gql_mutations import PolicyHolderInsureeUpdateInputType, \
    PolicyHolderContributionPlanUpdateInputType, PolicyHolderUserUpdateInputType, PolicyHolderUpdateInputType


class UpdatePolicyHolderMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "PolicyHolderMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolder

    class Input(PolicyHolderUpdateInputType):
        pass


class UpdatePolicyHolderInsureeMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "PolicyHolderInsureeMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolderInsuree

    class Input(PolicyHolderInsureeUpdateInputType):
        pass


class UpdatePolicyHolderContributionPlanMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "PolicyHolderContributionPlanMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolderContributionPlan

    class Input(PolicyHolderContributionPlanUpdateInputType):
        pass


class UpdatePolicyHolderUserMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "PolicyHolderUserMutation"
    _mutation_module = "policyholder"
    _model = PolicyHolderUser

    class Input(PolicyHolderUserUpdateInputType):
        pass

