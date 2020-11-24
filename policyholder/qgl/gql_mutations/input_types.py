import graphene
from core.schema import OpenIMISMutation, TinyInt


class PolicyHolderInputType(OpenIMISMutation.Input):
    id = graphene.UUID(required=False)

    code = graphene.String(max_length=255, required=True)
    trade_name = graphene.String(max_length=255, required=True)
    location_ids = graphene.List(graphene.Int)
    address = graphene.types.json.JSONString(max_length=255, required=False)
    phone = graphene.String(max_length=50, required=False)
    fax = graphene.String(max_length=50, required=False)
    email = graphene.String(max_length=255, required=False)
    contact_name = graphene.String(max_length=255, required=False)
    legal_form = graphene.Int(required=False)
    activity_code = graphene.Int(required=False)
    accountancy_account = graphene.String(required=False)
    bank_account = graphene.types.json.JSONString(required=False)
    payment_reference = graphene.String(required=False)
    json_ext = graphene.types.json.JSONString(required=False)


class PolicyHolderInsureeInputType(OpenIMISMutation.Input):
    id = graphene.UUID(required=False)

    policy_holder_id = graphene.UUID(required=False)
    insuree_id = graphene.Int(required=False)
    contribution_plan_bundle_id = graphene.Int(requried=False)
    last_policy_id = graphene.Int(required=False)
    json_ext = graphene.types.json.JSONString(required=False)


class PolicyHolderContributionPlanInputType(OpenIMISMutation.Input):
    id = graphene.Int(required=False)

    policy_holder_id = graphene.Int(required=False)
    contribution_plan_bundle_id = graphene.Int(requried=False)

    json_ext = graphene.types.json.JSONString(required=False)


class PolicyHolderUserInputType(OpenIMISMutation.Input):
    id = graphene.Int(required=False)

    user_id = graphene.Int(required=False)
    policy_holder_id = graphene.Int(required=False)

    json_ext = graphene.types.json.JSONString(required=False)
