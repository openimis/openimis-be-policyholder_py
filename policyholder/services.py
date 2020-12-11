import core
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import PermissionDenied
from django.db import connection, transaction
from django.contrib.auth.models import AnonymousUser
from django.core import serializers
from django.forms.models import model_to_dict
from policyholder.models import PolicyHolder as PolicyHolderModel, PolicyHolderUser as PolicyHolderUserModel, \
    PolicyHolderContributionPlan as PolicyHolderContributionPlanModel, PolicyHolderInsuree as PolicyHolderInsureeModel


class PolicyHolder(object):

    def __init__(self, user):
        self.user = user

    def get(self, limit=100, page=1, **kwargs):
         pass

    def get_by_id(self, by_policy_holder):
        if not self.user.id:
            return{
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
            }
        else:
            policy_holder = PolicyHolderModel.objects.get(id=by_policy_holder.id)
            return{
                "success": True,
                "message": "Ok",
                "detail": "",
                "data": serializers.serialize("json", policy_holder),
            }

    def create(self, policy_holder):
        if not self.user.id:
            return {
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
            }
        try:
            print(policy_holder)
            phm = PolicyHolderModel(**policy_holder)
            phm.save(username=self.user.username)
            uuid_string = str(phm.id)
            dict_representation = model_to_dict(phm)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return {
                "success": False,
                "message": "Failed to create PolicyHolder",
                "detail": str(exc),
                "data": "",
            }
        return {
            "success": True,
            "message": "Ok",
            "detail": "",
            "data": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
        }

    def update(self, policy_holder):
        if not self.user.id:
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
            uuid_string = str(updated_phm.id)
            dict_representation = model_to_dict(updated_phm)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return {
                "success": False,
                "message": "Failed to update PolicyHolder",
                "detail": str(exc),
                "data": "",
            }
        return {
            "success": True,
            "message": "Ok",
            "detail": "",
            "data": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
        }

    def delete(self, policy_holder):
        if not self.user.id:
            return {
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
                "data": "",
            }
        try:
            phm_to_delete = PolicyHolderModel.objects.filter(id=policy_holder['id']).first()
            phm_to_delete.delete(username=self.user.username)
            return {
                "success": True,
                "message": "Ok",
                "detail": "",
            }
        except Exception as exc:
            return{
                "success": False,
                "message": "Failed to delete PolicyHolder",
                "detail": str(exc),
                "data": "",
            }


class PolicyHolderInsuree(object):

    def __init__(self, user):
        self.user = user
        pass

    def create(self, policy_holder_insuree):
        if not self.user.id:
            return {
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
            }
        try:
            print(policy_holder_insuree)
            phim = PolicyHolderInsureeModel(**policy_holder_insuree)
            phim.save(username=self.user.username)
            uuid_string = str(phim.id)
            dict_representation = model_to_dict(phim)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return {
                "success": False,
                "message": "Failed to create PolicyHolderInsuree",
                "detail": str(exc),
                "data": "",
            }
        return {
            "success": True,
            "message": "Ok",
            "detail": "",
            "data": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
        }

    def update(self, policy_holder_insuree):
        if not self.user.id:
            return {
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
                "data": "",
            }
        try:
            updated_phim = PolicyHolderInsureeModel.objects.filter(id=policy_holder_insuree['id']).first()
            [setattr(updated_phim, key, policy_holder_insuree[key]) for key in policy_holder_insuree]
            updated_phim.save(username=self.user.username)
            uuid_string = str(updated_phim.id)
            dict_representation = model_to_dict(updated_phim)
            dict_representation["id"], dict_representation["uuid"] = (str(uuid_string), str(uuid_string))
        except Exception as exc:
            return {
                "success": False,
                "message": "Failed to update PolicyHolderInsuree",
                "detail": str(exc),
                "data": "",
            }
        return {
            "success": True,
            "message": "Ok",
            "detail": "",
            "data": json.loads(json.dumps(dict_representation, cls=DjangoJSONEncoder)),
        }

    def delete(self, policy_holder_insuree):
        if not self.user.id:
            return {
                "success": False,
                "message": "Authentication required",
                "detail": "PermissionDenied",
                "data": "",
            }
        try:
            phim_to_delete = PolicyHolderInsureeModel.objects.filter(id=policy_holder_insuree['id']).first()
            phim_to_delete.delete(username=self.user.username)
            return {
                "success": True,
                "message": "Ok",
                "detail": "",
            }
        except Exception as exc:
            return{
                "success": False,
                "message": "Failed to delete PolicyHolderInsuree",
                "detail": str(exc),
                "data": "",
            }

    def replace_policy_holder_insuree(self, policy_holder_insuree):
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