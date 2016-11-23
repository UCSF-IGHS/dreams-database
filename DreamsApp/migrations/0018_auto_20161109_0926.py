# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-09 09:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DreamsApp', '0017_auto_20161104_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='date_voided',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientdrugusedata',
            name='date_voided',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientdrugusedata',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientdrugusedata',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='clientdrugusedata',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clienteducationandemploymentdata',
            name='date_voided',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clienteducationandemploymentdata',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clienteducationandemploymentdata',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='clienteducationandemploymentdata',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientgenderbasedviolencedata',
            name='date_voided',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientgenderbasedviolencedata',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientgenderbasedviolencedata',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='clientgenderbasedviolencedata',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clienthivtestingdata',
            name='date_voided',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clienthivtestingdata',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clienthivtestingdata',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='clienthivtestingdata',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientindividualandhouseholddata',
            name='date_voided',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientindividualandhouseholddata',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientindividualandhouseholddata',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='clientindividualandhouseholddata',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientparticipationindreams',
            name='date_voided',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientparticipationindreams',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientparticipationindreams',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='clientparticipationindreams',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientreproductivehealthdata',
            name='date_voided',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientreproductivehealthdata',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientreproductivehealthdata',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='clientreproductivehealthdata',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientsexualactivitydata',
            name='date_voided',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientsexualactivitydata',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='clientsexualactivitydata',
            name='voided',
            field=models.BigIntegerField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='clientsexualactivitydata',
            name='voided_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='intervention',
            name='reason_voided',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]