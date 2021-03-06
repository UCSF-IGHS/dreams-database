# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-18 16:40
from __future__ import unicode_literals

from django.db import migrations, models
import uuid

from xf.uc_dashboards.models import Template


class Migration(migrations.Migration):

    def create_code(apps, schema_editor):
        for template in Template.objects.all():
            template.code = 'template-{}'.format(template.id)
            template.save()

    def remove_code(apps, schema_editor):
        pass

    dependencies = [
        ('uc_dashboards', '0022_merge_20180122_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='code',
            field=models.CharField(default=uuid.uuid4, help_text='User-defined code for this template', max_length=50),
        ),
        migrations.RunPython(create_code, remove_code),
    ]
