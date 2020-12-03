# Generated by Django 3.0.3 on 2020-11-26 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('policyholder', '0005_auto_20201125_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policyholder',
            name='user_created',
            field=models.ForeignKey(db_column='UserCreatedUUID', default='49a8342a-1ccc-45cc-968e-ed4d528577c5', on_delete=django.db.models.deletion.DO_NOTHING, related_name='policyholder_user_created', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='policyholder',
            name='user_updated',
            field=models.ForeignKey(db_column='UserUpdatedUUID', default='49a8342a-1ccc-45cc-968e-ed4d528577c5', on_delete=django.db.models.deletion.DO_NOTHING, related_name='policyholder_user_updated', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='policyholdercontributionplan',
            name='user_created',
            field=models.ForeignKey(db_column='UserCreatedUUID', default='49a8342a-1ccc-45cc-968e-ed4d528577c5', on_delete=django.db.models.deletion.DO_NOTHING, related_name='policyholdercontributionplan_user_created', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='policyholdercontributionplan',
            name='user_updated',
            field=models.ForeignKey(db_column='UserUpdatedUUID', default='49a8342a-1ccc-45cc-968e-ed4d528577c5', on_delete=django.db.models.deletion.DO_NOTHING, related_name='policyholdercontributionplan_user_updated', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='policyholderinsuree',
            name='user_created',
            field=models.ForeignKey(db_column='UserCreatedUUID', default='49a8342a-1ccc-45cc-968e-ed4d528577c5', on_delete=django.db.models.deletion.DO_NOTHING, related_name='policyholderinsuree_user_created', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='policyholderinsuree',
            name='user_updated',
            field=models.ForeignKey(db_column='UserUpdatedUUID', default='49a8342a-1ccc-45cc-968e-ed4d528577c5', on_delete=django.db.models.deletion.DO_NOTHING, related_name='policyholderinsuree_user_updated', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='policyholderuser',
            name='user_created',
            field=models.ForeignKey(db_column='UserCreatedUUID', default='49a8342a-1ccc-45cc-968e-ed4d528577c5', on_delete=django.db.models.deletion.DO_NOTHING, related_name='policyholderuser_user_created', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='policyholderuser',
            name='user_updated',
            field=models.ForeignKey(db_column='UserUpdatedUUID', default='49a8342a-1ccc-45cc-968e-ed4d528577c5', on_delete=django.db.models.deletion.DO_NOTHING, related_name='policyholderuser_user_updated', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]