# Generated by Django 4.2.9 on 2024-02-07 16:47

import core.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('policyholder', '0017_auto_20230126_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpolicyholder',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholder',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholder',
            name='replacement_uuid',
            field=models.UUIDField(blank=True, db_column='ReplacementUUID', null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholdercontributionplan',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholdercontributionplan',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholdercontributionplan',
            name='replacement_uuid',
            field=models.UUIDField(blank=True, db_column='ReplacementUUID', null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholderinsuree',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholderinsuree',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholderinsuree',
            name='replacement_uuid',
            field=models.UUIDField(blank=True, db_column='ReplacementUUID', null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholderuser',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholderuser',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalpolicyholderuser',
            name='replacement_uuid',
            field=models.UUIDField(blank=True, db_column='ReplacementUUID', null=True),
        ),
        migrations.AlterField(
            model_name='policyholder',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='policyholder',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='policyholder',
            name='replacement_uuid',
            field=models.UUIDField(blank=True, db_column='ReplacementUUID', null=True),
        ),
        migrations.AlterField(
            model_name='policyholder',
            name='user_created',
            field=models.ForeignKey(db_column='UserCreatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='policyholder',
            name='user_updated',
            field=models.ForeignKey(db_column='UserUpdatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='policyholdercontributionplan',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='policyholdercontributionplan',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='policyholdercontributionplan',
            name='replacement_uuid',
            field=models.UUIDField(blank=True, db_column='ReplacementUUID', null=True),
        ),
        migrations.AlterField(
            model_name='policyholdercontributionplan',
            name='user_created',
            field=models.ForeignKey(db_column='UserCreatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='policyholdercontributionplan',
            name='user_updated',
            field=models.ForeignKey(db_column='UserUpdatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='policyholderinsuree',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='policyholderinsuree',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='policyholderinsuree',
            name='replacement_uuid',
            field=models.UUIDField(blank=True, db_column='ReplacementUUID', null=True),
        ),
        migrations.AlterField(
            model_name='policyholderinsuree',
            name='user_created',
            field=models.ForeignKey(db_column='UserCreatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='policyholderinsuree',
            name='user_updated',
            field=models.ForeignKey(db_column='UserUpdatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='policyholderuser',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='policyholderuser',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='policyholderuser',
            name='replacement_uuid',
            field=models.UUIDField(blank=True, db_column='ReplacementUUID', null=True),
        ),
        migrations.AlterField(
            model_name='policyholderuser',
            name='user_created',
            field=models.ForeignKey(db_column='UserCreatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_user_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='policyholderuser',
            name='user_updated',
            field=models.ForeignKey(db_column='UserUpdatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_user_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]