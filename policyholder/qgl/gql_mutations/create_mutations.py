from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderContributionPlan, PolicyHolderUser
from policyholder.qgl.gql_mutations import PolicyHolderInputType, PolicyHolderInsureeInputType, \
    PolicyHolderContributionPlanInputType, PolicyHolderUserInputType
from policyholder.qgl.gql_mutations.base_mutation import BaseMutation, BaseCreateMutationMixin


class CreatePolicyHolderMutation(BaseMutation, BaseCreateMutationMixin):
    _mutation_class = "PolicyHolderMutation"
    _model = PolicyHolder

    class Input(PolicyHolderInputType):
        pass


class CreatePolicyHolderInsureeMutation(BaseMutation, BaseCreateMutationMixin):
    _mutation_class = "PolicyHolderInsureeMutation"
    _model = PolicyHolderInsuree

    class Input(PolicyHolderInsureeInputType):
        pass


class CreatePolicyHolderContributionPlanMutation(BaseMutation, BaseCreateMutationMixin):
    _mutation_class = "PolicyHolderContributionPlanMutation"
    _model = PolicyHolderContributionPlan

    class Input(PolicyHolderContributionPlanInputType):
        pass


class CreatePolicyHolderUserMutation(BaseMutation, BaseCreateMutationMixin):
    _mutation_class = "PolicyHolderUserMutation"
    _model = PolicyHolderUser

    class Input(PolicyHolderUserInputType):
        pass

