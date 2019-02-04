# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-05-17 12:59
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.core.management import call_command
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    def load_data(apps, schema_editor):
        call_command("loaddata", "configurable_parameters.json")

    dependencies = [
        ('DreamsApp', '0045_configurableparameter'),
    ]
