import xml.etree.ElementTree as ET
from django.core.exceptions import PermissionDenied
import core
from django.db import connection, transaction

from django.conf import settings


@core.comparable
class PolicyHolder(object):

    def __init__(self, policy_holder):
        self.policy_holder = policy_holder
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    @transaction.atomic
    def replace_policy_holder(self):
        pass

    @transaction.atomic
    def remove_policy_holder(self):
        pass


@core.comparable
class PolicyHolderInsuree(object):

    def __init__(self, policy_holder):
        self.policy_holder = policy_holder
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def create(self, insuree):
        pass

    def update(self, insuree):
        pass

    def replace_policy_holder_insuree(self, insuree):
        pass

    def remove_policy_holder_insuree(self, insuree):
        pass


@core.comparable
class PolicyHolderContributionPlan(object):

    def __init__(self, policy_holder):
        self.policy_holder = policy_holder
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def create(self, contribution_plan):
        pass

    def update(self, contribution_plan):
        pass

    def replace_plan(self, contribution_plan):
        pass

    def remove_plan(self, contribution_plan):
        pass


@core.comparable
class PolicyHolderUser(object):

    def __init__(self, policy_holder):
        self.policy_holder = policy_holder
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def create(self, user):
        pass

    def update(self, user):
        pass

    def delete(self, user):
        pass
