# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-19 14:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uc_dashboards', '0026_auto_20180619_1356'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='widget',
            unique_together=set([('slug',)]),
        ),
    ]
