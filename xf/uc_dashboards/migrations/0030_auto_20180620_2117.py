# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-20 21:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uc_dashboards', '0029_auto_20180619_1637'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='perspective',
            unique_together=set([('code',)]),
        ),
    ]
