from __future__ import unicode_literals
from DreamsApp.models import *
from DreamsApp.xf_test_case.xf_test_case import XFTestCase


class TestParentImplemetingPartnerTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parent_implementing_partner_is_optional(self):
        self.assertFieldOptional(ImplementingPartner, 'parent_implementing_partner', 'parent_implementing_partner is optional')
