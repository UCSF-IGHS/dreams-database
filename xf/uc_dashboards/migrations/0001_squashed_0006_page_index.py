# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 14:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('uc_dashboards', '0001_squashed_0052_auto_20161115_2238'), ('uc_dashboards', '0002_auto_20170808_1333'), ('uc_dashboards', '0003_auto_20170808_1657'), ('uc_dashboards', '0004_page_show_filter_bar'), ('uc_dashboards', '0005_auto_20170809_0717'), ('uc_dashboards', '0006_page_index')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavigationSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50)),
                ('index', models.IntegerField(default=0)),
                ('icon', models.CharField(blank=True, max_length=50)),
                ('parent_section', models.ForeignKey(blank=True, help_text='Specify a parent navigation section, or leave it empty if it is a top section', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_sections', to='uc_dashboards.NavigationSection')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('text', models.TextField(max_length=10400)),
                ('permissions_to_view', models.ManyToManyField(to='auth.Group')),
                ('allow_anonymous', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PageSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='section',
            field=models.ForeignKey(help_text='Taxonomy classification of this page. Helps to form a pretty URL.', on_delete=django.db.models.deletion.CASCADE, to='uc_dashboards.PageSection'),
        ),
        migrations.AlterField(
            model_name='page',
            name='permissions_to_view',
            field=models.ManyToManyField(blank=True, to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='page',
            name='text',
            field=models.TextField(blank=True, max_length=10400),
        ),
        migrations.AddField(
            model_name='page',
            name='main_title',
            field=models.CharField(help_text='Main title on top of the page', max_length=150),
        ),
        migrations.AddField(
            model_name='page',
            name='slug',
            field=models.SlugField(help_text='This field identifies part of the URL that makes it friendly', max_length=150),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('template_path', models.CharField(blank=True, max_length=255)),
                ('template_text', models.TextField(blank=True, help_text='Allows you to specificy the content of a template.')),
                ('template_type', models.CharField(choices=[('1', 'Page'), ('2', 'Dashboard'), ('3', 'Widget'), ('0', 'Other')], default='1', help_text='The type of template', max_length=2)),
                ('template_source', models.CharField(choices=[('1', 'File within Django app (template file)'), ('2', 'Load from database (specify here)')], default='1', help_text='Specifies whether the template should be loaded from the file system, or from the database.', max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(help_text='The template to be used to render this page. May be overridden by the view.', on_delete=django.db.models.deletion.CASCADE, to='uc_dashboards.Template'),
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('url_section', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='page_type',
            field=models.ForeignKey(help_text='Determines if this is a normal page, or a dashboard', on_delete=django.db.models.deletion.CASCADE, to='uc_dashboards.PageType'),
        ),
        migrations.AddField(
            model_name='page',
            name='page_id',
            field=models.CharField(blank=True, help_text='Can be used in the view to load a specific set of context data, e.g. a dashboard', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='navigation_section',
            field=models.ForeignKey(blank=True, help_text='Specifies the navigation item to link this item to. ', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page', to='uc_dashboards.NavigationSection'),
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the widget.', max_length=150)),
                ('slug', models.SlugField(help_text='This field identifies part of the URL that makes it friendly', max_length=150)),
                ('allow_anonymous', models.BooleanField(help_text='Specifies whether anonymous browsing is allowed for this widget')),
                ('widget_id', models.CharField(blank=True, help_text='Can be used in the view to load a specific set of context data', max_length=50, null=True)),
                ('permissions_to_view', models.ManyToManyField(blank=True, help_text='Specifies the groups that may view this widget', to='auth.Group')),
                ('template', models.ForeignKey(help_text='The template to be used to render this widget. May be overridden by the view.', on_delete=django.db.models.deletion.CASCADE, to='uc_dashboards.Template')),
                ('widget_type', models.CharField(choices=[('1', 'Pie'), ('2', 'Table'), ('3', 'Tiles'), ('4', 'Easy pie'), ('5', 'Line graph'), ('6', 'Bar graph'), ('7', 'Doughnut graph'), ('10', 'Progress circle'), ('8', 'Map'), ('9', 'Text block'), ('0', 'Other')], default='0', help_text='The type of widget', max_length=2)),
                ('data_columns', models.TextField(blank=True, help_text='Tables/Pie: Data columns to use. One per line. Must be a Python dictionary format.')),
                ('data_point_column', models.TextField(blank=True, help_text='Pie: the column that has the data points for a pie. Must be a Python dictionary format.')),
                ('sql_query', models.TextField(blank=True, help_text='Tables/Pie: The SQL query to run with this widget')),
                ('sub_text', models.TextField(blank=True, help_text='Pie: text to show below the pie.')),
                ('label_column', models.TextField(blank=True, help_text='Pie: the column that has the labels to be shown in the pie')),
                ('database_key', models.CharField(default='ptbi_data', help_text='The key from the settings file to use for the data connection for this widget.', max_length=150)),
                ('text', models.TextField(blank=True, help_text='If this is a text widget, the text will be displayed in the widget. Useful for static widgets.')),
                ('custom_attributes', models.TextField(blank=True, help_text='Any custom attributes. Must be a Python dictionary format.')),
                ('filters', models.CharField(blank=True, help_text='Quoted and comma-separated list of string values with filter names from the query string', max_length=512, null=True)),
                ('code', models.CharField(blank=True, help_text='A code that can be used to identify this widget. The code will be displayed in the "About this widget" box.', max_length=255)),
                ('user_description', models.TextField(blank=True, help_text='A description that helps the user understand what this widget shows. It will be shown in a pop-up window. ')),
                ('view_details_url', models.CharField(blank=True, help_text='A URL specifiying a details link. This could be another dashboard, or a JasperReport. ', max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='page',
            name='allow_anonymous',
            field=models.BooleanField(help_text='Specifies whether anonymous browsing is allowed for this page'),
        ),
        migrations.AlterField(
            model_name='page',
            name='permissions_to_view',
            field=models.ManyToManyField(blank=True, help_text='Specifies the groups that may view this page', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='page',
            name='text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(help_text='Title of the page. Also appears in the navigation bar.', max_length=150),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='navigationsection',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='navigation_sections', to='uc_dashboards.Tag'),
        ),
        migrations.AddField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='pages', to='uc_dashboards.Tag'),
        ),
        migrations.AddField(
            model_name='template',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='templates', to='uc_dashboards.Tag'),
        ),
        migrations.AddField(
            model_name='widget',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='widgets', to='uc_dashboards.Tag'),
        ),
        migrations.CreateModel(
            name='Perspective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of this perspective.', max_length=255)),
                ('comment', models.TextField(blank=True, help_text='Any comment.')),
                ('pages', models.ManyToManyField(blank=True, help_text='The pages that are part of this perspective.',
                                                 related_name='perspectives', to='uc_dashboards.Page')),
                ('tags', models.ManyToManyField(blank=True, related_name='perspectives', to='uc_dashboards.Tag')),
                ('code', models.CharField(blank=True,
                                          help_text='A code for this perspective. The code will be used to preset filters.',
                                          max_length=128)),
                ('default_page',
                 models.ForeignKey(help_text='The default page that will be displayed when a user logs on.',
                                   on_delete=django.db.models.deletion.CASCADE, to='uc_dashboards.Page')),
            ],
        ),
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, help_text='Any comment.')),
                ('tags', models.ManyToManyField(blank=True, related_name='group_profiles', to='uc_dashboards.Tag')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.Group')),
                ('preset_filters', models.TextField(blank=True, help_text='Can set preset filters for perspectives. Filters will be applied onto perspectives')),
                ('perspectives', models.ManyToManyField(blank=True, related_name='group_perspectives', to='uc_dashboards.Perspective')),
            ],
        ),
        migrations.AlterField(
            model_name='template',
            name='template_source',
            field=models.CharField(choices=[('1', 'File system'), ('2', 'From database')], default='1', help_text='Specifies whether the template should be loaded from the file system, or from the database.', max_length=2),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preset_filters', models.TextField(blank=True, help_text='Can set preset filters for perspectives. Filters will be applied onto perspectives')),
                ('comment', models.TextField(blank=True, help_text='Any comment.')),
                ('tags', models.ManyToManyField(blank=True, related_name='user_profiles', to='uc_dashboards.Tag')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
                ('default_perspective', models.ForeignKey(blank=True, help_text='The default perspective for this user. May be null if the user only has one perspective from their groups. If the perspective is not part of a group, the default perspective will be added.', null=True, on_delete=django.db.models.deletion.CASCADE, to='uc_dashboards.Perspective')),
            ],
        ),
        migrations.AlterField(
            model_name='perspective',
            name='default_page',
            field=models.ForeignKey(help_text='The default page that will be displayed when a user logs on.', on_delete=django.db.models.deletion.CASCADE, to='uc_dashboards.Page'),
        ),
        migrations.AlterField(
            model_name='widget',
            name='database_key',
            field=models.CharField(help_text='The key from the settings file to use for the data connection for this widget.', max_length=150),
        ),
        migrations.AlterField(
            model_name='widget',
            name='widget_type',
            field=models.CharField(choices=[('1', 'Pie'), ('2', 'Table'), ('3', 'Tiles'), ('4', 'Easy pie'), ('5', 'Line graph'), ('6', 'Bar graph'), ('7', 'Doughnut graph'), ('10', 'Progress circle'), ('8', 'Map'), ('9', 'Text block'), ('11', 'Filter drop down'), ('0', 'Other')], default='0', help_text='The type of widget', max_length=2),
        ),
        migrations.AddField(
            model_name='page',
            name='show_filter_bar',
            field=models.BooleanField(default=True, help_text='Check this field if you want to display the filter bar. Otherwise it will be hidden.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='parent_page',
            field=models.ForeignKey(blank=True, help_text='Specifies a parent page for this item. Leave this empty if a page is immediately below a navigation section ', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childma_page', to='uc_dashboards.Page'),
        ),
        migrations.AlterField(
            model_name='page',
            name='navigation_section',
            field=models.ForeignKey(blank=True, help_text='Specifies the navigation item to link this item to. Do not specify this if a parent page is set', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page', to='uc_dashboards.NavigationSection'),
        ),
        migrations.AddField(
            model_name='page',
            name='index',
            field=models.IntegerField(blank=True, default=0, help_text='Pages with a lower index will be added to the navigation tree before those with a higher index. This is used to sort the navigation tree.'),
        ),
    ]
