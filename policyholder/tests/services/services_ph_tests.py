from unittest import TestCase
from location.models import Location
from insuree.models import Insuree
from policyholder.services import PolicyHolder as PolicyHolderService, PolicyHolderInsuree as PolicyHolderInsureeService, \
    PolicyHolderContributionPlan as PolicyHolderContributionPlanService
from policyholder.models import PolicyHolder, PolicyHolderInsuree, PolicyHolderContributionPlan, PolicyHolderUser
from policyholder.tests.helpers import create_test_policy_holder, create_test_policy_holder_insuree

from contribution_plan.models import ContributionPlanBundle
from contribution_plan.tests.helpers_tests import create_test_contribution_plan_bundle
from policy.models import Policy
from insuree.test_helpers import create_test_insuree
from core.models import User


class ServiceTestPolicyHolder(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.get(username="admin")
        cls.policy_holder_service = PolicyHolderService(cls.user)
        cls.policy_holder_insuree_service = PolicyHolderInsureeService(cls.user)
        cls.policy_holder_contribution_plan_service = PolicyHolderContributionPlanService(cls.user)

        cls.test_policy_holder = create_test_policy_holder()
        cls.test_policy_holder_insuree = create_test_policy_holder_insuree()

        cls.test_insuree = cls.test_policy_holder_insuree.insuree
        cls.test_insuree_to_change = create_test_insuree()
        cls.test_contribution_plan_bundle = cls.test_policy_holder_insuree.contribution_plan_bundle
        cls.test_last_policy = cls.test_policy_holder_insuree.last_policy
        cls.test_contribution_plan_bundle_to_replace = create_test_contribution_plan_bundle()

    @classmethod
    def tearDownClass(cls):
        ph_insuree = PolicyHolderInsuree.objects.get(policy_holder=cls.test_policy_holder)
        PolicyHolderInsuree.objects.filter(id__in=[cls.test_policy_holder_insuree.id, ph_insuree.id]).delete()
        PolicyHolder.objects.filter(id=cls.test_policy_holder.id).delete()
        ContributionPlanBundle.objects.filter(id__in=[cls.test_contribution_plan_bundle.id, cls.test_contribution_plan_bundle_to_replace.id]).delete()

    def test_policy_holder_create(self):
        policy_holder = {
            'code': 'TT',
            'trade_name': 'COTO',
            'address': '{\"region\": \"APAC\", \"street\": \"test\"}',
            'phone': '111000111',
            'fax': 'Fax',
            'email': 'policy_holder@mail.com',
            'contact_name': '{\"name\": \"test\", \"surname\": \"test-test\"}',
            'legal_form': 1,
            'activity_code': 2,
            'accountancy_account': '128903719082739810273',
            'bank_account': "{ \"IBAN\": \"PL00 0000 2345 0000 1000 2345 2345\" }",
            'payment_reference': 'PolicyHolderPaymentReference',
        }
        response = self.policy_holder_service.create(policy_holder)

        # tear down the test data
        PolicyHolder.objects.filter(id=response["data"]["id"]).delete()

        self.assertEqual(
            (
                 True,
                 "Ok",
                 "",
                 "TT",
                 "COTO",
                 1,
                 "{ \"IBAN\": \"PL00 0000 2345 0000 1000 2345 2345\" }",
                 "128903719082739810273",
            ),
            (
                 response['success'],
                 response['message'],
                 response['detail'],
                 response['data']['code'],
                 response['data']['trade_name'],
                 response['data']['version'],
                 response['data']['bank_account'],
                 response['data']['accountancy_account'],
            )
        )

    def test_policy_holder_create_update(self):
        policy_holder = {
            'code': 'TT',
            'trade_name': 'COTO',
            'address': '{\"region\": \"APAC\", \"street\": \"test\"}',
            'phone': '111000111',
            'fax': 'Fax',
            'email': 'policy_holder@mail.com',
            'contact_name': '{\"name\": \"test\", \"surname\": \"test-test\"}',
            'legal_form': 1,
            'activity_code': 2,
            'accountancy_account': '128903719082739810273',
            'bank_account': "{ \"IBAN\": \"PL00 0000 2345 0000 1000 2345 2345\" }",
            'payment_reference': 'PolicyHolderPaymentReference',
        }
        response = self.policy_holder_service.create(policy_holder)
        policy_holder_object = PolicyHolder.objects.get(id=response['data']['id'])
        version = policy_holder_object.version
        policy_holder = {
            'id': str(policy_holder_object.id),
            'address': '{\"region\": \"TEST\", \"street\": \"TEST\"}',
        }
        response = self.policy_holder_service.update(policy_holder)

        # tear down the test data
        PolicyHolder.objects.filter(id=response["data"]["id"]).delete()

        self.assertEqual(
            (
                True,
                "Ok",
                "",
                '{\"region\": \"TEST\", \"street\": \"TEST\"}',
                2,
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response['data']['address'],
                response['data']['version'],
            )
        )

    def test_policy_holder_update_without_changing_field(self):
        policy_holder_object = self.test_policy_holder
        version = policy_holder_object.version
        policy_holder = {
            'id': str(policy_holder_object.id),
            'address': policy_holder_object.address,
        }
        response = self.policy_holder_service.update(policy_holder)
        self.assertEqual(
            (
                False,
                "Failed to update PolicyHolder",
                "['Record has not be updated - there are no changes in fields']",
            ),
            (
                response['success'],
                response['message'],
                response['detail']
            )
        )

    def test_policy_holder_update_without_id(self):
        policy_holder = {
            'address': '{\"region\": \"APAC\", \"street\": \"test\"}',
        }
        response = self.policy_holder_service.update(policy_holder)
        self.assertEqual(
            (
                False,
                "Failed to update PolicyHolder",
            ),
            (
                response['success'],
                response['message'],
            )
        )

    def test_policy_holder_create_delete(self):
        policy_holder = {
            'code': 'TT',
            'trade_name': 'COTO',
            'address': '{\"region\": \"APAC\", \"street\": \"test\"}',
            'phone': '111000111',
            'fax': 'Fax',
            'email': 'policy_holder@mail.com',
            'contact_name': '{\"name\": \"test\", \"surname\": \"test-test\"}',
            'legal_form': 1,
            'activity_code': 2,
            'accountancy_account': '128903719082739810273',
            'bank_account': "{ \"IBAN\": \"PL00 0000 2345 0000 1000 2345 2345\" }",
            'payment_reference': 'PolicyHolderPaymentReference',
        }
        response = self.policy_holder_service.create(policy_holder)
        policy_holder_object = PolicyHolder.objects.get(id=response['data']['id'])
        version = policy_holder_object.version
        policy_holder = {
            'id': str(policy_holder_object.id),
        }
        response = self.policy_holder_service.delete(policy_holder)

        # tear down the test data
        PolicyHolder.objects.filter(id=str(policy_holder_object.id)).delete()

        self.assertEqual(
            (
                True,
                "Ok",
                "",
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
            )
        )

    def test_policy_holder_insuree_create(self):
        policy_holder_insuree = {
            'policy_holder_id': str(self.test_policy_holder.id),
            'insuree_id': self.test_insuree.id,
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle.id),
            'last_policy_id': self.test_last_policy.id
        }

        response = self.policy_holder_insuree_service.create(policy_holder_insuree)

        # tear down the test data
        PolicyHolderInsuree.objects.filter(id=response["data"]["id"]).delete()

        self.assertEqual(
            (
                True,
                "Ok",
                "",
                1,
                str(self.test_policy_holder.id),
                self.test_insuree.id,
                str(self.test_contribution_plan_bundle.id),
                self.test_last_policy.id
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response['data']['version'],
                response['data']['policy_holder'],
                response['data']['insuree'],
                response['data']['contribution_plan_bundle'],
                response['data']['last_policy'],
            )
        )

    def test_policy_holder_insuree_create_without_fk(self):
        policy_holder_insuree = {
            'policy_holder_id': str(self.test_policy_holder.id),
        }

        response = self.policy_holder_insuree_service.create(policy_holder_insuree)
        self.assertEqual(
            (
                False,
                "Failed to create PolicyHolderInsuree",
            ),
            (
                response['success'],
                response['message'],
            )
        )

    def test_policy_holder_insuree_create_update(self):
        policy_holder_insuree = {
            'policy_holder_id': str(self.test_policy_holder.id),
            'insuree_id': self.test_insuree.id,
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle.id),
            'last_policy_id': self.test_last_policy.id
        }

        response = self.policy_holder_insuree_service.create(policy_holder_insuree)

        policy_holder_insuree_object = PolicyHolderInsuree.objects.get(id=response['data']['id'])
        policy_holder_insuree = {
            'id': str(policy_holder_insuree_object.id),
            'insuree_id': self.test_insuree_to_change.id,
        }
        response = self.policy_holder_insuree_service.update(policy_holder_insuree)

        # tear down the test data
        PolicyHolderInsuree.objects.filter(id=response["data"]["id"]).delete()

        self.assertEqual(
            (
                True,
                "Ok",
                "",
                self.test_insuree_to_change.id,
                2,
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response['data']['insuree'],
                response['data']['version'],
            )
        )

    def test_policy_holder_insuree_update_without_changing_field(self):
        policy_holder_insuree = {
            'id': str(self.test_policy_holder_insuree.id),
            'insuree_id': self.test_insuree.id,
        }
        response = self.policy_holder_insuree_service.update(policy_holder_insuree)
        self.assertEqual(
            (
                False,
                "Failed to update PolicyHolderInsuree",
                "['Record has not be updated - there are no changes in fields']",
            ),
            (
                response['success'],
                response['message'],
                response['detail']
            )
        )

    def test_policy_holder_insuree_update_without_id(self):
        policy_holder_insuree = {
            'insuree_id': self.test_insuree.id,
        }

        response = self.policy_holder_insuree_service.update(policy_holder_insuree)
        self.assertEqual(
            (
                False,
                "Failed to update PolicyHolderInsuree",
            ),
            (
                response['success'],
                response['message'],
            )
        )

    def test_policy_holder_insuree_replace(self):
        policy_holder_insuree = {
            'policy_holder_id': str(self.test_policy_holder.id),
            'insuree_id': self.test_insuree.id,
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle.id),
            'last_policy_id': self.test_last_policy.id
        }

        response = self.policy_holder_insuree_service.create(policy_holder_insuree)

        policy_holder_insuree_object = PolicyHolderInsuree.objects.get(id=response['data']['id'])
        policy_holder_insuree = {
            'uuid': str(policy_holder_insuree_object.id),
            'insuree_id': self.test_insuree_to_change.id,
            'contribution_plan_bundle_id': self.test_contribution_plan_bundle_to_replace.id
        }
        response = self.policy_holder_insuree_service.replace_policy_holder_insuree(policy_holder_insuree)

        # tear down the test data
        PolicyHolderInsuree.objects.filter(
            id__in=[str(policy_holder_insuree_object.id), response['uuid_new_object']]
        ).delete()

        self.assertEqual(
            (
                True,
                "Ok",
                "",
                response["old_object"]["replacement_uuid"],
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response["uuid_new_object"],
            )
        )

    def test_policy_holder_insuree_replace_double(self):
        policy_holder_insuree = {
            'policy_holder_id': str(self.test_policy_holder.id),
            'insuree_id': self.test_insuree.id,
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle.id),
            'last_policy_id': self.test_last_policy.id
        }

        response = self.policy_holder_insuree_service.create(policy_holder_insuree)

        policy_holder_insuree_object = PolicyHolderInsuree.objects.get(id=response['data']['id'])
        policy_holder_insuree = {
            'uuid': str(policy_holder_insuree_object.id),
            'insuree_id': self.test_insuree_to_change.id,
            'contribution_plan_bundle_id': self.test_contribution_plan_bundle_to_replace.id
        }
        id_first_object = str(policy_holder_insuree_object.id)
        response = self.policy_holder_insuree_service.replace_policy_holder_insuree(policy_holder_insuree)

        policy_holder_insuree_object = PolicyHolderInsuree.objects.get(id=response['uuid_new_object'])
        policy_holder_insuree = {
            'uuid': str(policy_holder_insuree_object.id),
            'insuree_id': self.test_insuree.id,
            'contribution_plan_bundle_id': self.test_contribution_plan_bundle.id
        }

        response = self.policy_holder_insuree_service.replace_policy_holder_insuree(policy_holder_insuree)

        # tear down the test data
        PolicyHolderInsuree.objects.filter(
            id__in=[str(policy_holder_insuree_object.id), response['uuid_new_object'], id_first_object]
        ).delete()

        self.assertEqual(
            (
                True,
                "Ok",
                "",
                response["old_object"]["replacement_uuid"],
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response["uuid_new_object"],
            )
        )

    def test_policy_holder_contribution_plan_create(self):
        policy_holder_contribution_plan = {
            'policy_holder_id': str(self.test_policy_holder.id),
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle.id),
        }

        response = self.policy_holder_contribution_plan_service.create(policy_holder_contribution_plan)

        # tear down the test data
        PolicyHolderContributionPlan.objects.filter(id=response["data"]["id"]).delete()

        self.assertEqual(
            (
                True,
                "Ok",
                "",
                1,
                str(self.test_policy_holder.id),
                str(self.test_contribution_plan_bundle.id),
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response['data']['version'],
                response['data']['policy_holder'],
                response['data']['contribution_plan_bundle'],
            )
        )

    def test_policy_holder_contribution_plan_create_without_fk(self):
        policy_holder_contribution_plan = {
            'policy_holder_id': str(self.test_policy_holder.id),
        }

        response = self.policy_holder_contribution_plan_service.create(policy_holder_contribution_plan)
        self.assertEqual(
            (
                False,
                "Failed to create PolicyHolderContributionPlan",
            ),
            (
                response['success'],
                response['message'],
            )
        )

    def test_policy_holder_contribution_plan_replace(self):
        policy_holder_contribution_plan = {
            'policy_holder_id': str(self.test_policy_holder.id),
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle.id),
        }

        response = self.policy_holder_contribution_plan_service.create(policy_holder_contribution_plan)

        policy_holder_contribution_plan_object = PolicyHolderContributionPlan.objects.get(id=response['data']['id'])
        policy_holder_contribution_plan = {
            'uuid': str(policy_holder_contribution_plan_object.id),
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle_to_replace.id),
        }

        response = self.policy_holder_contribution_plan_service.replace_policy_holder_contribution_plan_bundle(
            policy_holder_contribution_plan
        )

        # tear down the test data
        PolicyHolderContributionPlan.objects.filter(
            id__in=[str(policy_holder_contribution_plan_object.id), response['uuid_new_object']]
        ).delete()

        self.assertEqual(
            (
                True,
                "Ok",
                "",
                response["old_object"]["replacement_uuid"],
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response["uuid_new_object"],
            )
        )

    def test_policy_holder_contribution_plan_replace_double(self):
        policy_holder_contribution_plan = {
            'policy_holder_id': str(self.test_policy_holder.id),
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle.id),
        }

        response = self.policy_holder_contribution_plan_service.create(policy_holder_contribution_plan)

        policy_holder_contribution_plan_object = PolicyHolderContributionPlan.objects.get(id=response['data']['id'])
        policy_holder_contribution_plan = {
            'uuid': str(policy_holder_contribution_plan_object.id),
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle_to_replace.id),
        }
        id_first_object = str(policy_holder_contribution_plan_object.id)
        response = self.policy_holder_contribution_plan_service.replace_policy_holder_contribution_plan_bundle(
            policy_holder_contribution_plan
        )

        policy_holder_contribution_plan_object = PolicyHolderContributionPlan.objects.get(id=response['uuid_new_object'])
        policy_holder_contribution_plan = {
            'uuid': str(policy_holder_contribution_plan_object.id),
            'contribution_plan_bundle_id': str(self.test_contribution_plan_bundle.id),
        }
        response = self.policy_holder_contribution_plan_service.replace_policy_holder_contribution_plan_bundle(policy_holder_contribution_plan)

        # tear down the test data
        PolicyHolderContributionPlan.objects.filter(
            id__in=[str(policy_holder_contribution_plan_object.id), response['uuid_new_object'], id_first_object]
        ).delete()

        self.assertEqual(
            (
                True,
                "Ok",
                "",
                response["old_object"]["replacement_uuid"],
            ),
            (
                response['success'],
                response['message'],
                response['detail'],
                response["uuid_new_object"],
            )
        )