from django.db.models import Q
from payment.apps import PaymentConfig
from payment.models import Payment
from .apps import PolicyholderConfig


def append_policy_holder_filter(sender, **kwargs):
    # OFS-257: Create dynamic filters for the payment mutation
    user = kwargs.get("user", None)
    additional_filter = kwargs.get('additional_filter', None)
    filters = kwargs.get('filters', None)
    filter_ph = None
    if user and filters:
        if "policyHolder" in additional_filter:
            # then check perms
            # TODO add in if statement the checking for portal payment perms
            if user.has_perms(PaymentConfig.gql_query_payments_perms) or user.has_perms(PolicyholderConfig.gql_query_payment_portal_perms):
                ph_id = additional_filter["policyHolder"]
                filter_ph = Q(payment_details__premium__contract_contribution_plan_details__contract_details__contract__policy_holder__id=ph_id)
    if filter_ph:
        filters.append(filter_ph)
