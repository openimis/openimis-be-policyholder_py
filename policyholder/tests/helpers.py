import json

from contribution_plan.tests.helpers import create_test_contribution_plan_bundle
from core.models import InteractiveUser, User, Officer, TechnicalUser
from insuree.test_helpers import create_test_insuree
from location.models import Location
from policy.test_helpers import create_test_policy

from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderUser
from datetime import date

from product.test_helpers import create_test_product


def create_test_policy_holder(locations=None, custom_parameters={}):
    user = __get_or_create_simple_policy_holder_user()

    object_data = {
        'code': 'PHCode',
        'version': 1,
        'trade_name': 'PolicyHolderTradeName',
        'address': 'PolicyHolderAddress',
        'phone': '111000111',
        'fax': 'Policy Holder Fax',
        'email': 'policy_holder@mail.com',
        'contact_name': 'PolicyHolderContractName',
        'legal_form': 1,
        'activity_code': 2,
        'accountancy_account': '128903719082739810273',
        'payment_reference': 'PolicyHolderPaymentReference',
        'date_created': date(2010, 10, 30),
        'date_updated': date(2010, 11, 30),
        'user_updated': user,
        'user_created': user,
        'date_valid_from': date(2010, 11, 30),
        'date_valid_to': None,
        'active': True,
        'json_ext': json.dumps("{}"),
        **custom_parameters
    }

    policy_holder = PolicyHolder.objects.create(**object_data)
    if locations:
        policy_holder.locations_uuid.set(locations)
    else:
        location = Location.objects.first()
        policy_holder.locations_uuid.add(location)

    policy_holder.save()
    return policy_holder


def create_test_policy_holder_insuree(policy_holder=None, insuree=None, contribution_plan_bundle=None,
                                      last_policy=None, custom_parameters={}):
    if not policy_holder:
        policy_holder = create_test_policy_holder()
    if not insuree:
        insuree = create_test_insuree()
    if not contribution_plan_bundle:
        contribution_plan_bundle = create_test_contribution_plan_bundle()
    if not last_policy:
        last_policy = create_test_policy(
            product=create_test_product("TestCode"),
            insuree=insuree)

    user = __get_or_create_simple_policy_holder_user()

    object_data = {
        'version': 1,
        'policy_holder': policy_holder,
        'insuree': insuree,
        'contribution_plan_bundle': contribution_plan_bundle,
        'last_policy': last_policy,
        'json_ext': json.dumps("{}"),
        'date_created': date(2010, 10, 30),
        'date_updated': date(2010, 10, 31),
        'user_updated': user,
        'user_created': user,
        **custom_parameters
    }

    return PolicyHolderInsuree.objects.create(**object_data)


def create_test_policy_holder_user(user=None, policy_holder=None, custom_parameters={}):
    if not user:
        user = __get_or_create_simple_policy_holder_user()

    if not policy_holder:
        policy_holder = create_test_policy_holder()

    audit_user = __get_or_create_simple_policy_holder_user()

    object_data = {
        'user': user,
        'policy_holder': policy_holder,
        'json_ext': json.dumps("{}"),
        'date_created': date(2010, 10, 30),
        'date_updated': date(2010, 10, 31),
        'user_updated': audit_user,
        'user_created': audit_user,
        'date_valid_from': date(2010, 10, 30),
        'date_valid_to': None,
        'active': 1,
        **custom_parameters
    }

    return PolicyHolderUser.objects.create(**object_data)


def __get_or_create_simple_policy_holder_user():
    user, _ = User.objects.get_or_create(username='policy_holder_user',
                                      i_user=InteractiveUser.objects.first())
    return user
