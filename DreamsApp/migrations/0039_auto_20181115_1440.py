# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-11-15 14:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0038_add_exit_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='exited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exited_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]