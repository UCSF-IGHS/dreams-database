from __future__ import unicode_literals
from DreamsApp.models import *
from xf.xf_system.tests.test_xf_test_case import XFTestCase


class TestImplementingPartnerTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_implementing_partner_is_optional(self):
        self.assertFieldOptional(Intervention, 'implementing_partner', 'implementing_partner is optional')
