from __future__ import unicode_literals
from DreamsApp.models import *
from django.test import TestCase


class TestImplementingPartnerTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_implementing_partner_is_optional(self):
        self.assertFieldOptional(Intervention, 'implementing_partner', 'implementing_partner is optional')
