# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-16 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uc_dashboards', '0019_auto_20171114_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='perspective',
            name='slug',
            field=models.SlugField(blank=True, help_text='This field identifies part of the URL that makes it friendly', max_length=150, null=True),
        ),
    ]
