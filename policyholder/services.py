import core

from django.core.exceptions import PermissionDenied
from django.db import connection, transaction
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core import serializers

from policyholder.models import PolicyHolder as PolicyHolderModel, PolicyHolderUser as PolicyHolderUserModel, \
    PolicyHolderContributionPlan as PolicyHolderContributionPlanModel, PolicyHolderInsuree as PolicyHolderInsureeManager


class PolicyHolder(object):

    def __init__(self, user):
        self.user = user

    def get(self, policy_holder):
        pass

    def create(self, policy_holder):
        if type(self.user) is AnonymousUser or not self.user.id:
            return {
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
            }
        try:
            phm = PolicyHolderModel(**policy_holder)
            phm.save(username=self.user.username)
            return {
                "success": True,
                "message": "Ok",
                "detail": serializers.serialize("json", phm),
                "data": "",
            }
        except Exception as exc:
            return{
                "success": False,
                "message": "Failed to create PolicyHolder",
                "detail": str(exc),
                "data": "",
            }

    def update(self, policy_holder):
        if type(self.user) is AnonymousUser or not self.user.id:
            return {
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
                "data": "",
            }
        try:
            updated_phm = PolicyHolderModel.objects.filter(id=policy_holder['id']).first()
            [setattr(updated_phm, key, policy_holder[key]) for key in policy_holder]
            updated_phm.save(username=self.user.username)
            return {
                "success": True,
                "message": "Ok",
                "detail": "",
                "data": serializers.serialize("json", updated_phm),
            }
        except Exception as exc:
            return{
                "success": False,
                "message": "Failed to create PolicyHolder",
                "detail": str(exc),
                "data": "",
            }

    def delete(self, policy_holder):
        pass

    def replace_policy_holder(self, policy_holder):
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

    def delete(self, insuree):
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

    def delete(self, contribution_plan):
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
