from __future__ import unicode_literals
from DreamsApp.models import ServiceDelegation
from xf.xf_system.tests.test_xf_test_case import XFTestCase
import datetime


class TestEndDateTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_end_date_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'end_date', 'delegation end_date is required')

