# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-04 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xf_system', '0006_auto_20170814_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='xfsitesettings',
            name='custom_theme',
            field=models.CharField(blank=True, help_text='Custom theme defined for the site.', max_length=50, null=True),
        ),
    ]
