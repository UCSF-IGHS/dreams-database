from __future__ import unicode_literals
from DreamsApp.models import *
from django.test import TestCase
import datetime


class TestInterventionDateTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_intervention_date_is_required(self):
        self.assertFieldRequired(Intervention, 'intervention_date', 'intervention_date is required')

    def test_greater_than_today(self):
        self.assertFieldNotClean(Intervention, 'intervention_date',
                                 datetime.date.today() + datetime.timedelta(days=1),
                                 'intervention_date cannot be later than today')

    def test_equal_to_today(self):
        self.assertFieldClean(Intervention, 'intervention_date',
                              datetime.date.today(),
                              'intervention_date cannot be equal to today')

    def test_less_than_today(self):
        self.assertFieldClean(Intervention, 'intervention_date',
                              datetime.date.today() - datetime.timedelta(days=1),
                              'intervention_date cannot be later than today')
