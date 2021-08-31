from __future__ import unicode_literals
from DreamsApp.models import *
from django.test import TestCase


class TestImplemetingPartnerFunderTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_implementing_partner_funder_is_optional(self):
        self.assertFieldOptional(ImplementingPartner, 'implementing_partner_funder', 'implementing_partner_funder is optional')
