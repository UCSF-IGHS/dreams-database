# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-02-01 07:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0041_auto_20190123_1401'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFollowUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_followup', models.DateField(verbose_name='Date of Followup')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Comment')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_follow_up', to='DreamsApp.Client')),
                ('result_of_followup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_of_followup', to='DreamsApp.ClientLTFUResultType')),
            ],
            options={
                'verbose_name': 'Client Follow Up',
                'verbose_name_plural': 'Client Follow Ups',
            },
        ),
        migrations.CreateModel(
            name='ClientFollowUpType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Follow Up Type',
                'verbose_name_plural': 'Follow Up Types',
            },
        ),
        migrations.RemoveField(
            model_name='clientltfu',
            name='client',
        ),
        migrations.RemoveField(
            model_name='clientltfu',
            name='result_of_followup',
        ),
        migrations.RemoveField(
            model_name='clientltfu',
            name='type_of_followup',
        ),
        migrations.DeleteModel(
            name='ClientLTFU',
        ),
        migrations.DeleteModel(
            name='ClientLTFUType',
        ),
        migrations.AddField(
            model_name='clientfollowup',
            name='type_of_followup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_up_type', to='DreamsApp.ClientFollowUpType'),
        ),
    ]
