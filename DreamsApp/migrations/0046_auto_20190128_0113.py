# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-27 22:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0045_client_ltfuresulttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfollowup',
            name='result_of_followup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_of_followup', to='DreamsApp.ClientLTFUResultType'),
        ),
    ]
