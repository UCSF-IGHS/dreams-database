# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-30 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uc_dashboards', '0006_auto_20171030_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widget',
            name='widget_type',
            field=models.CharField(choices=[('1', 'Pie'), ('2', 'Table'), ('3', 'Tiles'), ('4', 'Easy pie'), ('5', 'Line graph'), ('6', 'Bar graph Vertical'), ('12', 'Bar graph Horizontal'), ('7', 'Doughnut graph'), ('10', 'Progress circle'), ('8', 'Map'), ('9', 'Text block'), ('11', 'Filter drop down'), ('13', 'Gauge'), ('0', 'Other')], default='0', help_text='The type of widget', max_length=2),
        ),
    ]
