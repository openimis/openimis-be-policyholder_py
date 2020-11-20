import graphene
from core.schema import OpenIMISMutation, TinyInt


class PolicyHolderInputType(OpenIMISMutation.Input):
    id = graphene.Int(required=False)

    code = graphene.String(max_length=255)
    version = graphene.Int(required=True)
    trade_name = graphene.Int(required=True)
    location_ids = graphene.List(graphene.Int)
    address = graphene.String(max_length=255, required=False)
    phone = graphene.String(max_length=50, required=False)
    fax = graphene.String(max_length=50, required=False)
    email = graphene.String(max_length=255, required=False)
    contract_name = graphene.String(max_length=255, required=False)
    legal_form = graphene.Int(required=False)
    activity_code = graphene.Int(required=False)
    accountancy_account = graphene.Int(required=False)
    payment_reference = graphene.Int(required=False)

    date_created = graphene.DateTime(required=False)
    date_updated = graphene.DateTime(required=False)

    user_updated = graphene.Int(required=False)
    user_created = graphene.Int(required=False)

    date_valid_from = graphene.DateTime(required=False)
    date_valid_to = graphene.DateTime(required=False)

    active = graphene.Boolean()
    json_ext = graphene.types.json.JSONString(required=False)


class PolicyHolderInsureeInputType(OpenIMISMutation.Input):
    id = graphene.Int(required=False)
    version = graphene.Int(required=True)

    policy_holder_id = graphene.Int(required=False)
    insuree_id = graphene.Int(required=False)
    contribution_plan_bundle_id = graphene.Int(requried=False)
    last_policy_id = graphene.Int(required=False)
    json_ext = graphene.types.json.JSONString(required=False)

    date_created = graphene.DateTime(required=False)
    date_updated = graphene.DateTime(required=False)

    user_updated = graphene.Int(required=False)
    user_created = graphene.Int(required=False)


class PolicyHolderContributionPlanInputType(OpenIMISMutation.Input):
    id = graphene.Int(required=False)
    version = graphene.Int(required=True)

    policy_holder_id = graphene.Int(required=False)
    contribution_plan_bundle_id = graphene.Int(requried=False)

    json_ext = graphene.types.json.JSONString(required=False)

    date_created = graphene.DateTime(required=False)
    date_updated = graphene.DateTime(required=False)

    user_updated = graphene.Int(required=False)
    user_created = graphene.Int(required=False)

    date_valid_from = graphene.DateTime(required=False)
    date_valid_to = graphene.DateTime(required=False)


class PolicyHolderUserInputType(OpenIMISMutation.Input):
    id = graphene.Int(required=False)
    version = graphene.Int(required=True)

    user_id = graphene.Int(required=False)
    policy_holder_id = graphene.Int(required=False)

    json_ext = graphene.types.json.JSONString(required=False)

    date_created = graphene.DateTime(required=False)
    date_updated = graphene.DateTime(required=False)

    user_updated = graphene.Int(required=False)
    user_created = graphene.Int(required=False)

    date_valid_from = graphene.DateTime(required=False)
    date_valid_to = graphene.DateTime(required=False)

    active = graphene.Boolean()
