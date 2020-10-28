# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2020-03-06 12:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0047_client_ltfuresulttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='date_of_birth',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='client',
            name='date_of_enrollment',
            field=models.DateField(blank=True, db_index=True, default=datetime.datetime.now, null=True, verbose_name='Date of Enrollment'),
        ),
        migrations.AlterField(
            model_name='client',
            name='dreams_id',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='DREAMS ID'),
        ),
        migrations.AlterField(
            model_name='client',
            name='exited',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='middle_name',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Middle Name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='ovc_id',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='voided',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='implementingpartner',
            name='name',
            field=models.CharField(db_index=True, max_length=150, verbose_name='Implementing Partner Name'),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='intervention_date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='interventioncategory',
            name='code',
            field=models.IntegerField(db_index=True, default=0, verbose_name='Intervention Category Code'),
        ),
        migrations.AlterField(
            model_name='interventiontype',
            name='code',
            field=models.IntegerField(db_index=True, default=0, verbose_name='Intervention Type Code'),
        ),
    ]