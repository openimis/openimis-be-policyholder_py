import graphene
import graphene_django_optimizer as gql_optimizer
from core.schema import OrderedDjangoFilterConnectionField
from rest_framework.exceptions import PermissionDenied
from policyholder.gql_queries import *


class Query(graphene.ObjectType):
    policy_holder = OrderedDjangoFilterConnectionField(PolicyHolderGQLType)

    def resolve_policy_holder(self, info, **kwargs):
        # if not info.context.user.has_perms(ClaimConfig.gql_query_claims_perms):
        #     raise PermissionDenied("unauthorized")
        query = PolicyHolder.objects
        return gql_optimizer.query(query.all(), info)