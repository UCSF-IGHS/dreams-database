# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-27 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0042_client_followuptype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientfollowup',
            options={'verbose_name': 'Client Follow Up', 'verbose_name_plural': 'Client Follow Ups'},
        ),
        migrations.AddField(
            model_name='clientfollowup',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Comment'),
        ),
    ]
