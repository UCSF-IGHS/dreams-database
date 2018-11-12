# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-11-12 12:26
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    def load_data(apps, schema_editor):
        call_command("loaddata", "client_ltf_type.json")

    dependencies = [
        ('DreamsApp', '0035_populate_external_organisations'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientLTFUType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=10, verbose_name='County Code')),
                ('name', models.CharField(default='', max_length=100, verbose_name='County')),
            ],
            options={
                'verbose_name': 'County',
                'verbose_name_plural': 'Counties',
            },
        ),
        migrations.AlterField(
            model_name='clientltfu',
            name='type_of_followup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ltfu_type', to='DreamsApp.ClientLTFUType'),
        ),
        migrations.AlterField(
            model_name='referralstatus',
            name='code',
            field=models.IntegerField(unique=True, verbose_name='Referral Code'),
        ),
        migrations.AlterField(
            model_name='referralstatus',
            name='name',
            field=models.CharField(default='Pending', max_length=20, unique=True, verbose_name='Referral Name'),
        ),
    ]
