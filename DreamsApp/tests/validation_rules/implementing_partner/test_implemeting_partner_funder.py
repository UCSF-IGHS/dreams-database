from __future__ import unicode_literals
from DreamsApp.models import *
from xf.xf_system.tests.test_xf_test_case import XFTestCase


class TestImplemetingPartnerFunderTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_implementing_partner_funder_is_optional(self):
        self.assertFieldOptional(ImplementingPartner, 'implementing_partner_funder', 'implementing_partner_funder is optional')
