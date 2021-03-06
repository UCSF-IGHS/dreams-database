# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-12-17 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('uc_dashboards', '0040_xfvizsitesettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the dataset. Shows in dropdown lists', max_length=150)),
                ('code', models.CharField(help_text='A code that can be used to uniquely identify this dataset.', max_length=255)),
                ('dataset_type', models.CharField(choices=[('1', 'SQL'), ('2', 'Custom built')], default='1', help_text='The type of dataset', max_length=2)),
                ('custom_daset_loader', models.CharField(blank=True, help_text='Only for complex datasets that are built in code. Provide a fully qualified class that implements XFCustomDataSetLoaderBase', max_length=255)),
                ('allow_anonymous', models.BooleanField(help_text='Specifies whether anonymous access is allowed for this dataset')),
                ('external_source_url', models.CharField(blank=True, help_text='A URL specifiying a REST API link. Use this if data will be queried externally', max_length=255)),
                ('sql_query', models.TextField(blank=True, help_text='The SQL query to run to get the data. Use this if data will be queried from database specified by the database key below')),
                ('filters', models.CharField(blank=True, help_text='Quoted and comma-separated list of string values with filter names from the query string', max_length=512, null=True)),
                ('database_key', models.CharField(blank=True, help_text='The key from the settings file to use for the data connection for this widget.', max_length=150)),
                ('custom_attributes', models.TextField(blank=True, help_text='Any custom attributes. Must be a Python dictionary format.')),
                ('permissions_to_view', models.ManyToManyField(blank=True, help_text='Specifies the groups that may access this dataset', to='auth.Group')),
            ],
        ),
        migrations.AddField(
            model_name='widget',
            name='dataset',
            field=models.ForeignKey(blank=True, help_text='A previously prepared dataset that will be used to load the data.', null=True, on_delete=django.db.models.deletion.CASCADE, to='uc_dashboards.DataSet'),
        ),
        migrations.AlterUniqueTogether(
            name='dataset',
            unique_together=set([('code',)]),
        ),
    ]
