# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-11-05 14:54
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations, models


class Migration(migrations.Migration):
    def load_data(apps, schema_editor):
        call_command("loaddata", "client_ltfu_resulttype.json")

    dependencies = [
        ('DreamsApp', '0044_auto_20190127_2235'),
    ]
