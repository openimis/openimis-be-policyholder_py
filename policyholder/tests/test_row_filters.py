"""get_queryset honours the OP-2029 validity contract (epic OP-3317, phase 1).

Explicit validity values return the expected rows; a caller asking for
nothing gets what it got before the contract existed.
"""

from django.test import TestCase

from core.test_helpers import assert_row_filters, create_test_interactive_user, mark_deleted
from policyholder.models import PolicyHolder
from policyholder.tests.helpers import create_test_policy_holder


class PolicyHolderRowFiltersTest(TestCase):
    def test_policy_holder(self):
        user = create_test_interactive_user(username="phrowfilters")
        live = create_test_policy_holder(custom_props={"code": "RWF1"})
        deleted = mark_deleted(create_test_policy_holder(custom_props={"code": "RWF2"}))
        assert_row_filters(
            self, PolicyHolder, PolicyHolder.objects.filter(id__in=[live.id, deleted.id]), user,
            live.id, deleted.id, default_hides_deleted=False,
        )
