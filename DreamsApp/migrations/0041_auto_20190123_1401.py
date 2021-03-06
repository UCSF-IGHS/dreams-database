# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-01-23 11:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DreamsApp', '0040_merge_20181214_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientLTFUResultType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'LTFU Result Type',
                'verbose_name_plural': 'LTFU Result Types',
            },
        ),
        migrations.AlterField(
            model_name='clientltfu',
            name='result_of_followup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_of_followup', to='DreamsApp.ClientLTFUResultType'),
        ),
        migrations.AlterField(
            model_name='clientltfu',
            name='type_of_followup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_of_followup', to='DreamsApp.ClientLTFUType'),
        ),
        migrations.AlterField(
            model_name='clientltfutype',
            name='code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='clientltfutype',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
