# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-19 16:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uc_dashboards', '0028_auto_20180619_1547'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pagestatus',
            unique_together=set([('code',)]),
        ),
    ]
