# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-07 22:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import xf.uc_dashboards.models


class Migration(migrations.Migration):

    dependencies = [
        ('uc_dashboards', '0009_auto_20171107_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Code of the status.', max_length=50)),
                ('name', models.CharField(help_text='Name of the status.', max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='data_sources',
            field=xf.uc_dashboards.models.HTMLField(blank=True, help_text='Specify the data sources for this page, if applicable.', null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='page_status',
            field=models.ForeignKey(blank=True, help_text='Specifies a the status of this page', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_status', to='uc_dashboards.PageStatus'),
        ),
    ]
