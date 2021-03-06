# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-02 08:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DreamsApp', '0014_auto_20161102_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervention',
            name='date_voided',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voided_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
