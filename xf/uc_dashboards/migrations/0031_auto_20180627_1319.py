# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-27 13:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uc_dashboards', '0030_auto_20180620_2117'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('text',)]),
        ),
    ]
