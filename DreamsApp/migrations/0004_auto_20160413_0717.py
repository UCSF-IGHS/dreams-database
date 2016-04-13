# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 07:17
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DreamsApp', '0003_auto_20160413_0659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervention',
            name='user',
        ),
        migrations.AddField(
            model_name='intervention',
            name='changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='intervention',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='intervention',
            name='date_changed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]