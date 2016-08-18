# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-27 06:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DreamsApp', '0008_auto_20160427_0609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='date_at_enrollment',
        ),
        migrations.AddField(
            model_name='client',
            name='date_of_enrollment',
            field=models.DateField(null=True, verbose_name='Date of Enrollment'),
        ),
        migrations.AddField(
            model_name='client',
            name='dreams_id',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='DREAMS ID'),
        ),
        migrations.AddField(
            model_name='client',
            name='enrolled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='guardian_name',
            field=models.CharField(blank=True, default='', max_length=250, null=True,
                                   verbose_name="Primary care give / Guardian' name"),
        ),
        migrations.AddField(
            model_name='client',
            name='guardian_national_id',
            field=models.CharField(blank=True, default='', max_length=10, null=True,
                                   verbose_name='National ID (Care giver / Guardian)'),
        ),
        migrations.AddField(
            model_name='client',
            name='guardian_phone_number',
            field=models.CharField(blank=True, max_length=13, null=True,
                                   verbose_name='Phone Number(Care giver / Guardian)'),
        ),
        migrations.AddField(
            model_name='client',
            name='informal_settlement',
            field=models.CharField(blank=True, default='', max_length=250, null=True,
                                   verbose_name='Informal Settlement'),
        ),
        migrations.AddField(
            model_name='client',
            name='landmark',
            field=models.CharField(blank=True, default='', max_length=250, null=True,
                                   verbose_name='Land mark near residence'),
        ),
        migrations.AddField(
            model_name='client',
            name='relationship_with_guardian',
            field=models.CharField(blank=True, default='', max_length=50, null=True,
                                   verbose_name='Relationship with Guardian'),
        ),
        migrations.AddField(
            model_name='client',
            name='village',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Village'),
        ),
    ]
