from __future__ import unicode_literals
from DreamsApp.models import *
from DreamsApp.xf_test_case.xf_test_case import XFTestCase


class TestImplementingPartnerTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_implementing_partner_is_required(self):
        self.assertFieldRequired(Intervention, 'implementing_partner', 'implementing_partner is required')
