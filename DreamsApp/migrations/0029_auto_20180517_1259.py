# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-05-17 12:59
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.core.management import call_command
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    def load_data(apps, schema_editor):
        call_command("loaddata", "client_transfer_status.json")

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DreamsApp', '0028_auto_20180423_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_changed', models.DateTimeField(auto_now=True, null=True)),
                ('transfer_reason', models.TextField(blank=True, max_length=255, null=True)),
                ('reject_reason', models.TextField(blank=True, max_length=255, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DreamsApp.Client')),
                ('completed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='completed_by', to=settings.AUTH_USER_MODEL)),
                ('destination_implementing_partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_implementing_partner', to='DreamsApp.ImplementingPartner')),
                ('initiated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_by', to=settings.AUTH_USER_MODEL)),
                ('source_implementing_partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_implementing_partner', to='DreamsApp.ImplementingPartner')),
            ],
            options={
                'verbose_name': 'Client Transfer',
                'verbose_name_plural': 'Client Transfers',
            },
        ),
        migrations.CreateModel(
            name='ClientTransferStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(0)])),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='clienttransfer',
            name='transfer_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='DreamsApp.ClientTransferStatus'),
        ),
        migrations.RunPython(load_data),
    ]