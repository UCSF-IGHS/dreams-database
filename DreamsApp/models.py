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
        verbose_name_plural = 'Women'


class InterventionCategory(models.Model):
    code = models.IntegerField(verbose_name='Intervention Category Code')
    name = models.CharField(max_length=30)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Intervention Category'
        verbose_name_plural = 'Intervention Categories'


class InterventionType(models.Model):
    code = models.IntegerField(verbose_name='Intervention Type Code', null=False, blank=False)
    name = models.CharField(max_length=30, null=False)
    intervention_category = models.ForeignKey(InterventionCategory, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Intervention Type'
        verbose_name_plural = 'Intervention Types'


class HIVTestResult(models.Model):
    code = models.IntegerField(name='code', verbose_name='HIV Test Result Code')
    name = models.CharField(max_length=20, verbose_name='HIV Test Result')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'HIV Test Result'
        verbose_name_plural = 'HIV Test Results'


class Intervention(models.Model):
    date_completed = models.DateField()
    woman = models.ForeignKey(Woman)
    user = models.ForeignKey(User)
    intervention_type = models.ForeignKey(InterventionType, null=True)
    hiv_test_result = models.ForeignKey(HIVTestResult)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Intervention'
        verbose_name_plural = 'Interventions'
