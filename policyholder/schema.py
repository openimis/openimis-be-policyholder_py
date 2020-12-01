import graphene
import graphene_django_optimizer as gql_optimizer

from core.schema import OrderedDjangoFilterConnectionField
from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderUser, PolicyHolderContributionPlan
from policyholder.gql.gql_mutations.create_mutations import CreatePolicyHolderMutation, \
    CreatePolicyHolderInsureeMutation, CreatePolicyHolderUserMutation, CreatePolicyHolderContributionPlanMutation
from policyholder.gql.gql_mutations.delete_mutations import DeletePolicyHolderMutation, \
    DeletePolicyHolderInsureeMutation, DeletePolicyHolderUserMutation, DeletePolicyHolderContributionPlanMutation
from policyholder.gql.gql_mutations.update_mutations import UpdatePolicyHolderMutation, \
    UpdatePolicyHolderInsureeMutation, UpdatePolicyHolderUserMutation, UpdatePolicyHolderContributionPlanMutation
from policyholder.gql.gql_mutations.replace_mutation import ReplacePolicyHolderMutation, ReplacePolicyHolderInsureeMutation, \
    ReplacePolicyHolderContributionPlanMutation, ReplacePolicyHolderUserMutation


from policyholder.gql.gql_types import PolicyHolderUserGQLType, PolicyHolderGQLType, PolicyHolderInsureeGQLType, \
    PolicyHolderContributionPlanGQLType

class Query(graphene.ObjectType):
    policy_holder = OrderedDjangoFilterConnectionField(PolicyHolderGQLType)
    policy_holder_insuree = OrderedDjangoFilterConnectionField(PolicyHolderInsureeGQLType)
    policy_holder_user = OrderedDjangoFilterConnectionField(PolicyHolderUserGQLType)
    policy_holder_contribution_plan_bundle = OrderedDjangoFilterConnectionField(PolicyHolderContributionPlanGQLType)

    def resolve_policy_holder(self, info, **kwargs):
        query = PolicyHolder.objects
        return gql_optimizer.query(query.all(), info)

    def resolve_policy_holder_insuree(self, info, **kwargs):
        query = PolicyHolderInsuree.objects
        return gql_optimizer.query(query.all(), info)

    def resolve_policy_holder_user(self, info, **kwargs):
        query = PolicyHolderUser.objects
        return gql_optimizer.query(query.all(), info)

    def resolve_policy_holder_contribution_plan_bundle(self, info, **kwargs):
        query = PolicyHolderContributionPlan.objects
        return gql_optimizer.query(query.all(), info)


class Mutation(graphene.ObjectType):
    create_policy_holder = CreatePolicyHolderMutation.Field()
    create_policy_holder_insuree = CreatePolicyHolderInsureeMutation.Field()
    create_policy_holder_user = CreatePolicyHolderUserMutation.Field()
    create_policy_holder_contribution_plan_bundle = CreatePolicyHolderContributionPlanMutation.Field()
        
    update_policy_holder = UpdatePolicyHolderMutation.Field()
    update_policy_holder_insuree = UpdatePolicyHolderInsureeMutation.Field()
    update_policy_holder_user = UpdatePolicyHolderUserMutation.Field()
    update_policy_holder_contribution_plan_bundle = UpdatePolicyHolderContributionPlanMutation.Field()       
    
    delete_policy_holder = DeletePolicyHolderMutation.Field()
    delete_policy_holder_insuree = DeletePolicyHolderInsureeMutation.Field()
    delete_policy_holder_user = DeletePolicyHolderUserMutation.Field()
    delete_policy_holder_contribution_plan_bundle = DeletePolicyHolderContributionPlanMutation.Field()

    replace_policy_holder = ReplacePolicyHolderMutation.Field()
    replace_policy_holder_insuree = ReplacePolicyHolderInsureeMutation.Field()
    replace_policy_holder_user = ReplacePolicyHolderUserMutation.Field()
    replace_policy_holder_contribution_plan_bundle = ReplacePolicyHolderContributionPlanMutation.Field()