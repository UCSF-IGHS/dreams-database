# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-27 05:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0005_auto_20160414_1150'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Woman',
            new_name='Client',
        ),
    ]
