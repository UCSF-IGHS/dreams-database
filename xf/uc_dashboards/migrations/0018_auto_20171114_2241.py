# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-14 22:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uc_dashboards', '0017_template_built_in'),
    ]

    operations = [
        migrations.RenameField(
            model_name='navigationsection',
            old_name='caption_en_uk',
            new_name='caption_en_gb',
        ),
        migrations.RenameField(
            model_name='navigationsection',
            old_name='caption_nl_nl',
            new_name='caption_nl',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='about_en_uk',
            new_name='about_en_gb',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='about_nl_nl',
            new_name='about_nl',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='data_sources_en_uk',
            new_name='data_sources_en_gb',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='data_sources_nl_nl',
            new_name='data_sources_nl',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='main_title_en_uk',
            new_name='main_title_en_gb',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='main_title_nl_nl',
            new_name='main_title_nl',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='text_en_uk',
            new_name='text_en_gb',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='text_nl_nl',
            new_name='text_nl',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='title_en_uk',
            new_name='title_en_gb',
        ),
        migrations.RenameField(
            model_name='page',
            old_name='title_nl_nl',
            new_name='title_nl',
        ),
        migrations.RenameField(
            model_name='pagesection',
            old_name='title_en_uk',
            new_name='title_en_gb',
        ),
        migrations.RenameField(
            model_name='pagesection',
            old_name='title_nl_nl',
            new_name='title_nl',
        ),
        migrations.RenameField(
            model_name='pagestatus',
            old_name='name_en_uk',
            new_name='name_en_gb',
        ),
        migrations.RenameField(
            model_name='pagestatus',
            old_name='name_nl_nl',
            new_name='name_nl',
        ),
        migrations.RenameField(
            model_name='perspective',
            old_name='name_en_uk',
            new_name='name_en_gb',
        ),
        migrations.RenameField(
            model_name='perspective',
            old_name='name_nl_nl',
            new_name='name_nl',
        ),
        migrations.RenameField(
            model_name='widget',
            old_name='sub_text_en_uk',
            new_name='sub_text_en_gb',
        ),
        migrations.RenameField(
            model_name='widget',
            old_name='sub_text_nl_nl',
            new_name='sub_text_nl',
        ),
        migrations.RenameField(
            model_name='widget',
            old_name='text_en_uk',
            new_name='text_en_gb',
        ),
        migrations.RenameField(
            model_name='widget',
            old_name='text_nl_nl',
            new_name='text_nl',
        ),
        migrations.RenameField(
            model_name='widget',
            old_name='title_en_uk',
            new_name='title_en_gb',
        ),
        migrations.RenameField(
            model_name='widget',
            old_name='title_nl_nl',
            new_name='title_nl',
        ),
        migrations.RenameField(
            model_name='widget',
            old_name='user_description_en_uk',
            new_name='user_description_en_gb',
        ),
        migrations.RenameField(
            model_name='widget',
            old_name='user_description_nl_nl',
            new_name='user_description_nl',
        ),
    ]
