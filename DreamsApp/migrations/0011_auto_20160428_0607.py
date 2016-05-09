# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 06:07
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0010_auto_20160427_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='age_at_enrollment',
            field=models.IntegerField(default=10, null=True, verbose_name='Age at Enrollment'),
        ),
        migrations.AlterField(
            model_name='client',
            name='county_of_residence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DreamsApp.County', verbose_name='County of residence'),
        ),
        migrations.AlterField(
            model_name='client',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name='Date Of Birth'),
        ),
        migrations.AlterField(
            model_name='client',
            name='date_of_enrollment',
            field=models.DateField(default=datetime.datetime.now, null=True, verbose_name='Date of Enrollment'),
        ),
        migrations.AlterField(
            model_name='client',
            name='dreams_id',
            field=models.CharField(max_length=50, null=True, verbose_name='DREAMS ID'),
        ),
        migrations.AlterField(
            model_name='client',
            name='dss_id_number',
            field=models.CharField(max_length=50, null=True, verbose_name='DSS ID Number'),
        ),
        migrations.AlterField(
            model_name='client',
            name='enrolled_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(max_length=100, null=True, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='guardian_name',
            field=models.CharField(max_length=250, null=True, verbose_name="Primary care give / Guardian' name"),
        ),
        migrations.AlterField(
            model_name='client',
            name='guardian_national_id',
            field=models.CharField(max_length=10, null=True, verbose_name='National ID (Care giver / Guardian)'),
        ),
        migrations.AlterField(
            model_name='client',
            name='guardian_phone_number',
            field=models.CharField(max_length=13, null=True, verbose_name='Phone Number(Care giver / Guardian)'),
        ),
        migrations.AlterField(
            model_name='client',
            name='informal_settlement',
            field=models.CharField(max_length=250, null=True, verbose_name='Informal Settlement'),
        ),
        migrations.AlterField(
            model_name='client',
            name='is_date_of_birth_estimated',
            field=models.BooleanField(verbose_name='Date of Birth Estimated'),
        ),
        migrations.AlterField(
            model_name='client',
            name='landmark',
            field=models.CharField(max_length=250, null=True, verbose_name='Land mark near residence'),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='marital_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DreamsApp.MaritalStatus', verbose_name='Marital Status'),
        ),
        migrations.AlterField(
            model_name='client',
            name='middle_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Middle Name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=13, null=True, verbose_name='Phone Number(Client)'),
        ),
        migrations.AlterField(
            model_name='client',
            name='relationship_with_guardian',
            field=models.CharField(max_length=50, null=True, verbose_name='Relationship with Guardian'),
        ),
        migrations.AlterField(
            model_name='client',
            name='sub_county',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DreamsApp.SubCounty', verbose_name='Sub County'),
        ),
        migrations.AlterField(
            model_name='client',
            name='verification_doc_no',
            field=models.CharField(max_length=50, null=True, verbose_name='Verification Doc. No.'),
        ),
        migrations.AlterField(
            model_name='client',
            name='village',
            field=models.CharField(max_length=250, null=True, verbose_name='Village'),
        ),
        migrations.AlterField(
            model_name='client',
            name='ward',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='DreamsApp.Ward', verbose_name='Ward'),
        ),
    ]