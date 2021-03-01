from __future__ import unicode_literals
from DreamsApp.models import ServiceDelegation
from xf.xf_system.tests.test_xf_test_case import XFTestCase
import datetime


class TestFinancialYearTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_financial_year_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'financial_year', 'financial year is required')

