from __future__ import unicode_literals
from DreamsApp.models import ServiceDelegation
from xf.xf_system.tests.test_xf_test_case import XFTestCase


class TestDelegatedImplementingPartnerTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_intervention_type_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'intervention_type', 'intervention type is required')

    def test_main_implementing_partner_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'delegated_implementing_partner', 'delegated implementing partner is required')

    def test_delegated_implementing_partner_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'delegated_implementing_partner', 'delegated implementing partner is required')

    def test_start_date_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'start_date', 'delegation start_date is required')

    def test_end_date_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'end_date', 'delegation end_date is required')

    def test_financial_year_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'financial_year', 'financial year is required')
    