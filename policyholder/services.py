import xml.etree.ElementTree as ET
from django.core.exceptions import PermissionDenied
import core
from django.db import connection, transaction

from django.conf import settings


@core.comparable
class PolicyHolder(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


@core.comparable
class PolicyHolderInsuree(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        pass

    def replace(self):
        return replace_policy_holder_insuree()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


@core.comparable
class PolicyHolderContributionPlan(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def replace(self):
        return replace_policy_holder_contribution_plan()

@core.comparable
class PolicyHolderUser(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


@transaction.atomic
def replace_policy_holder(**kwargs):
    pass


@transaction.atomic
def replace_policy_holder_contribution_plan(**kwargs):
    pass


@transaction.atomic
def replace_policy_holder_insuree(**kwargs):
    pass
