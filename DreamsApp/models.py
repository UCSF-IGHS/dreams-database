from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Woman(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    middle_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    date_of_birth = models.DateField(verbose_name='Date Of Birth')

    def __str__(self):
        return '{}'.format(self.first_name)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class InterventionCategory(models.Model):
    code = models.IntegerField(verbose_name='Intervention Category Code', default=0)
    name = models.CharField(max_length=30)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Intervention Category'
        verbose_name_plural = 'Intervention Categories'


class InterventionType(models.Model):
    code = models.IntegerField(verbose_name='Intervention Type Code', default=0, null=False, blank=False)
    name = models.CharField(max_length=30, null=False)
    intervention_category = models.ForeignKey(InterventionCategory, null=False, blank=False)
    has_hts_result = models.BooleanField(default=False);
    has_pregnancy_result = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Intervention Type'
        verbose_name_plural = 'Intervention Types'


class HTSResult(models.Model):
    code = models.IntegerField(name='code', verbose_name='HTS Result Code')
    name = models.CharField(max_length=20, verbose_name='HTS Result Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'HTS Result'
        verbose_name_plural = 'HTS Results'

class PregnancyTestResult(models.Model):
    code = models.IntegerField(name='code', verbose_name='Pregnancy Result Code')
    name = models.CharField(max_length=20, verbose_name='Pregnancy Result Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Pregnancy Result'
        verbose_name_plural = 'Pregnancy Results'


class Intervention(models.Model):
    intervention_date = models.DateField()
    client = models.ForeignKey(Woman)
    user = models.ForeignKey(User)
    intervention_type = models.ForeignKey(InterventionType, null=True, blank=True)
    hts_result = models.ForeignKey(HTSResult, null=True, blank=True)
    pregnancy_test_result = models.ForeignKey(PregnancyTestResult, null=True, blank=True)
    client_ccc_number = models.CharField(max_length=11, blank=True, null=True)
    date_linked_to_ccc = models.DateField(blank=True, null=True)
    no_of_sessions_attended = models.IntegerField(null=True, blank=True)
    comment = models.TextField(max_length=256, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Intervention'
        verbose_name_plural = 'Interventions'

