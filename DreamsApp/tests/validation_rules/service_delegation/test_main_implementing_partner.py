from __future__ import unicode_literals
from DreamsApp.models import ServiceDelegation
from xf.xf_system.tests.test_xf_test_case import XFTestCase


class TestMainImplementingPartnerTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main_implementing_partner_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'main_implementing_partner', 'main implementing partner is required')