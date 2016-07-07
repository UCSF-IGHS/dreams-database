# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-07 01:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0019_intervention_implementing_partner'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=100, verbose_name='Code')),
                ('name', models.CharField(default='', max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'User Role',
                'verbose_name_plural': 'User Roles',
            },
        ),
        migrations.AddField(
            model_name='implementingpartneruser',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DreamsApp.UserRole'),
        ),
    ]
