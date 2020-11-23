import graphene
from contribution_plan.gql import ContributionPlanBundleGQLType
from core import prefix_filterset, ExtendedConnection
from graphene_django import DjangoObjectType
from insuree.schema import InsureeGQLType
from location.gql_queries import LocationGQLType

from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderUser, PolicyHolderContributionPlan


class PolicyHolderGQLType(DjangoObjectType):

    class Meta:
        model = PolicyHolder
        exclude_fields = ('row_id',)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "code": ["exact", "istartswith", "icontains", "iexact"],
            "version": ["exact"],
            "trade_name": ["exact", "istartswith", "icontains", "iexact"],
            "address": ["exact", "istartswith", "icontains", "iexact"],
            "phone": ["exact", "istartswith", "icontains", "iexact"],
            "fax": ["exact", "istartswith", "icontains", "iexact"],
            "email": ["exact", "istartswith", "icontains", "iexact"],
            "contact_name": ["exact", "istartswith", "icontains", "iexact"],
            "legal_form": ["exact"],
            "activity_code": ["exact"],
            "accountancy_account": ["exact"],
            "payment_reference": ["exact"],
            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "date_valid_from": ["exact", "lt", "lte", "gt", "gte"],
            "date_valid_to": ["exact", "lt", "lte", "gt", "gte"],
            "is_deleted": ["exact"]
        }

        connection_class = ExtendedConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return PolicyHolder.get_queryset(queryset, info)


class PolicyHolderInsureeGQLType(DjangoObjectType):

    class Meta:
        model = PolicyHolderInsuree
        exclude_fields = ('row_id',)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "version": ["exact"],
            **prefix_filterset("policy_holder__", PolicyHolderGQLType._meta.filter_fields),
            **prefix_filterset("insuree__", InsureeGQLType._meta.filter_fields),
            **prefix_filterset("contribution_plan_bundle__", ContributionPlanBundleGQLType._meta.filter_fields),
            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "user_created": ["exact"],
            "user_updated": ["exact"],
            #**prefix_filterset("location__", LocationGQLType._meta.filter_fields)
        }

        connection_class = ExtendedConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return PolicyHolder.get_queryset(queryset, info)


class PolicyHolderContributionPlanGQLType(DjangoObjectType):

    class Meta:
        model = PolicyHolderContributionPlan
        exclude_fields = ('row_id',)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "version": ["exact"],

            **prefix_filterset("policy_holder__", PolicyHolderGQLType._meta.filter_fields),
            **prefix_filterset("contribution_plan_bundle__", ContributionPlanBundleGQLType._meta.filter_fields),

            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "user_created": ["exact"],
            "user_updated": ["exact"],
            "date_valid_from": ["exact", "lt", "lte", "gt", "gte"],
            "date_valid_to": ["exact", "lt", "lte", "gt", "gte"],
            "is_deleted": ["exact"],
        }

        connection_class = ExtendedConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return PolicyHolder.get_queryset(queryset, info)


class PolicyHolderUserGQLType(DjangoObjectType):

    class Meta:
        model = PolicyHolderUser
        exclude_fields = ('row_id',)
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "user": ["exact"],
            **prefix_filterset("policy_holder__", PolicyHolderGQLType._meta.filter_fields),

            "date_created": ["exact", "lt", "lte", "gt", "gte"],
            "date_updated": ["exact", "lt", "lte", "gt", "gte"],
            "user_created": ["exact"],
            "user_updated": ["exact"],
            "date_valid_from": ["exact", "lt", "lte", "gt", "gte"],
            "date_valid_to": ["exact", "lt", "lte", "gt", "gte"],
            "is_deleted": ["exact"],
        }

        connection_class = ExtendedConnection

    @classmethod
    def get_queryset(cls, queryset, info):
        return PolicyHolder.get_queryset(queryset, info)
