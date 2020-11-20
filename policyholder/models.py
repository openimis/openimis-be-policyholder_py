import uuid

from contribution_plan.models import ContributionPlanBundle
from django.conf import settings
from django.db import models
from core import models as core_models, fields
from graphql import ResolveInfo
from jsonfallback.fields import FallbackJSONField
from location.models import Location
from insuree.models import Insuree
from policy.models import Policy


class PolicyHolderManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(PolicyHolderManager, self).filter(*args, **kwargs)


class PolicyHolder(core_models.HistoryBusinessModel):
    uuid = models.CharField(db_column='PolicyHolderUUID', max_length=36, default=uuid.uuid4, unique=True)
    code = models.CharField(db_column='PolicyHolderCode', max_length=32, blank=True, null=True)
    trade_name = models.CharField(db_column='TradeName', max_length=256)
    locations_uuid = models.ManyToManyField(Location, verbose_name="LocationsUUID", blank=True)
    address = models.CharField(db_column='Address', max_length=1024)
    phone = models.CharField(db_column='Phone', max_length=16)
    fax = models.CharField(db_column='Fax', max_length=16)
    email = models.CharField(db_column='Email', max_length=256)
    contact_name = models.CharField(db_column='ContractName', max_length=256)
    legal_form = models.IntegerField(db_column='LegalForm')
    activity_code = models.IntegerField(db_column='ActivityCode')
    accountancy_account = models.CharField(db_column='AccountancyAccount', max_length=255)
    payment_reference = models.CharField(db_column='PaymentReference', max_length=255)

    active = models.BooleanField(db_column='Active')

    objects = PolicyHolderManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=-1)
        if settings.ROW_SECURITY:
            pass
        return queryset

    class Meta:
        db_table = 'tblPolicyHolder'


class PolicyHolderInsureeManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(PolicyHolderInsureeManager, self).filter(*args, **kwargs)


class PolicyHolderInsuree(core_models.HistoryBusinessModel):
    uuid = models.CharField(db_column='PolicyHolderInsureeUUID', max_length=36, default=uuid.uuid4, unique=True)
    policy_holder = models.ForeignKey(PolicyHolder, db_column='PolicyHolderId',
                                      on_delete=models.deletion.DO_NOTHING)
    insuree = models.ForeignKey(Insuree, db_column='InsureeId',
                                on_delete=models.deletion.DO_NOTHING)
    contribution_plan_bundle = models.ForeignKey(ContributionPlanBundle, db_column='ContribuiotnPlanBundleId',
                                                 on_delete=models.deletion.DO_NOTHING)
    last_policy = models.ForeignKey(Policy, db_column='LastPolicyId', on_delete=models.deletion.DO_NOTHING)


    user_updated = models.ForeignKey(core_models.User, db_column="UserUpdatedUUID",related_name="%(class)s_UpdatedUUID",
                                    on_delete=models.deletion.DO_NOTHING, null=True)
    user_created = models.ForeignKey(core_models.User, db_column="UserCreatedUUID",related_name="%(class)s_CreatedUUID",
                                    on_delete=models.deletion.DO_NOTHING)

    objects = PolicyHolderInsureeManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=-1)
        if settings.ROW_SECURITY:
            pass
        return queryset

    class Meta:
        db_table = 'tblPolicyHolderInsuree'


class PolicyHolderContributionPlanManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(PolicyHolderContributionPlanManager, self).filter(*args, **kwargs)


class PolicyHolderContributionPlan(core_models.HistoryBusinessModel):
    uuid = models.CharField(db_column='PolicyHolderContributionPlanUUID', max_length=36, default=uuid.uuid4, unique=True)
    policy_holder = models.ForeignKey(PolicyHolder, db_column='PolicyHolderId',
                                      on_delete=models.deletion.DO_NOTHING)
    contribution_plan_bundle = models.ForeignKey(ContributionPlanBundle, db_column='ContribuiotnPlanBundleId',
                                                 on_delete=models.deletion.DO_NOTHING)

    user_updated = models.ForeignKey(core_models.User, db_column="UserUpdatedUUID",related_name="%(class)s_UpdatedUUID",
                                    on_delete=models.deletion.DO_NOTHING, null=True)
    user_created = models.ForeignKey(core_models.User, db_column="UserCreatedUUID",related_name="%(class)s_CreatedUUID",
                                    on_delete=models.deletion.DO_NOTHING)
    active = models.BooleanField(db_column='Active')

    objects = PolicyHolderContributionPlanManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=-1)
        if settings.ROW_SECURITY:
            pass
        return queryset

    class Meta:
        db_table = 'tblPolicyHolderContributionPlan'


class PolicyHolderUserManager(models.Manager):
    def filter(self, *args, **kwargs):
        keys = [x for x in kwargs if "itemsvc" in x]
        for key in keys:
            new_key = key.replace("itemsvc", self.model.model_prefix)
            kwargs[new_key] = kwargs.pop(key)
        return super(PolicyHolderUserManager, self).filter(*args, **kwargs)


class PolicyHolderUser(core_models.HistoryBusinessModel):
    uuid = models.CharField(db_column='PolicyHolderUserUUID', max_length=36, default=uuid.uuid4, unique=True)
    user = models.ForeignKey(core_models.User, db_column='UserUUID',
                                                 on_delete=models.deletion.DO_NOTHING)
    policy_holder = models.ForeignKey(PolicyHolder, db_column='PolicyHolderId',
                                      on_delete=models.deletion.DO_NOTHING)
    user_updated = models.ForeignKey(core_models.User, db_column="UserUpdatedUUID",
                                     related_name="%(class)s_UpdatedUUID", on_delete=models.deletion.DO_NOTHING)
    user_created = models.ForeignKey(core_models.User, db_column="UserCreatedUUID",
                                     related_name="%(class)s_CreatedUUID", on_delete=models.deletion.DO_NOTHING)
    active = models.BooleanField(db_column='Active')

    objects = PolicyHolderUserManager()

    @classmethod
    def get_queryset(cls, queryset, user):
        queryset = cls.filter_queryset(queryset)
        if isinstance(user, ResolveInfo):
            user = user.context.user
        if settings.ROW_SECURITY and user.is_anonymous:
            return queryset.filter(id=-1)
        if settings.ROW_SECURITY:
            pass
        return queryset

    class Meta:
        db_table = 'tblPolicyHolderUser'
