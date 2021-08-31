from __future__ import unicode_literals
from DreamsApp.models import *
from django.test import TestCase


class TestInterventionTypeTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_intervention_type_is_optional(self):
        self.assertFieldOptional(Intervention, 'intervention_type', 'intervention_type is optional')
