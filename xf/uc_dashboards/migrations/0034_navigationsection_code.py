# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-28 13:47
from __future__ import unicode_literals

from django.db import migrations, models
import uuid

from xf.uc_dashboards.models import NavigationSection


class Migration(migrations.Migration):
    def create_code(apps, schema_editor):
        for navigation_section in NavigationSection.objects.all():
            navigation_section.code = "navigation-section-{}".format(navigation_section.id)
            navigation_section.save()

    def remove_code(apps, schema_editor):
        pass

    dependencies = [
        ('uc_dashboards', '0033_auto_20180628_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigationsection',
            name='code',
            field=models.CharField(default=uuid.uuid4, help_text='User-defined code for this template', max_length=50),
        ),
        migrations.RunPython(create_code, remove_code)
    ]
