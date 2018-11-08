from __future__ import unicode_literals
from DreamsApp.models import *
from DreamsApp.xf_test_case.xf_test_case import XFTestCase
import datetime


class TestInterventionDateTestCase(XFTestCase):
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
