# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2020-11-17 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0048_auto_20200306_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervention',
            name='odk_uuid',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
