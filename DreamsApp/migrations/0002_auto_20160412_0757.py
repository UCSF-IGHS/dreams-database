# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-12 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='woman',
            options={'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.AddField(
            model_name='interventiontype',
            name='has_hts_result',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='interventiontype',
            name='has_pregnancy_result',
            field=models.BooleanField(default=False),
        ),
    ]