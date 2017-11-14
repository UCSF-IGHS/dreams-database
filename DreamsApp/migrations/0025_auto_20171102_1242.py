# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-02 12:42
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DreamsApp', '0024_auto_20170104_0515'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditTrail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column', models.CharField(max_length=50)),
                ('old_value', models.CharField(blank=True, max_length=250, null=True)),
                ('new_value', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Audit Trail',
                'verbose_name_plural': 'Audit Trails',
            },
        ),
        migrations.CreateModel(
            name='InterventionTypeAlternative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='-', max_length=250, verbose_name='Service name')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='Service description')),
                ('package_option_category', models.IntegerField(choices=[(1, 'Required Service'), (2, 'Situation Based Service')], default=1, verbose_name='Package option category')),
                ('intervention_type_alternatives_text', models.TextField(blank=True, null=True, verbose_name='Intervention type alternatives')),
                ('intervention_type_alternatives', models.ManyToManyField(to='DreamsApp.InterventionType', verbose_name='Intervention type alternatives')),
            ],
            options={
                'verbose_name': 'Service Package Intervention Alternative',
                'verbose_name_plural': 'Service Package Interventions Alternatives',
            },
        ),
        migrations.CreateModel(
            name='ServicePackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, verbose_name='Name')),
                ('description', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Description')),
                ('lower_age_limit', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(24)], verbose_name='Lower age limit')),
                ('upper_age_limit', models.PositiveIntegerField(default=24, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(24)], verbose_name='Upper age limit')),
                ('age_group', models.CharField(blank=True, default='-', max_length=5, null=True, verbose_name='Age group')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('date_changed', models.DateTimeField(auto_now=True, null=True, verbose_name='Date changed')),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Changed by')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'verbose_name': 'Service Package',
                'verbose_name_plural': 'Service Packages',
            },
        ),
        migrations.CreateModel(
            name='ServicePackageInterventionTypeAlternative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intervention_type_alternative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DreamsApp.InterventionTypeAlternative', verbose_name='Service package intervention alternative')),
                ('service_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DreamsApp.ServicePackage')),
            ],
        ),
        migrations.AddField(
            model_name='audit',
            name='column',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='audit',
            name='new_value',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='audit',
            name='old_value',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='servicepackage',
            name='intervention_type_alternatives',
            field=models.ManyToManyField(through='DreamsApp.ServicePackageInterventionTypeAlternative', to='DreamsApp.InterventionTypeAlternative', verbose_name='Service package intervention types'),
        ),
        migrations.AddField(
            model_name='audittrail',
            name='audit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DreamsApp.Audit'),
        ),
    ]
