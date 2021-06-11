from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.contrib.auth.models import User

from DreamsApp.models import ServiceDelegation, ImplementingPartner, InterventionType
from xf.xf_system.tests.test_xf_test_case import XFTestCase


class TestDelegatedImplementingPartnerTestCase(XFTestCase):
    fixtures = ['test_verification_document', 'test_marital_status', 'test_user', 'test_intervention_category',
                'test_intervention_type', 'test_county',
                'implementing_partner_funder', 'test_implementing_partner', 'external_organisation_type',
                'external_organisation', 'test_sub_county', 'test_ward', 'test_client', 'test_hts_result',
                'test_pregnancy_test_result']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_intervention_type_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'intervention_type', 'intervention type is required')

    def test_main_implementing_partner_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'delegated_implementing_partner',
                                 'delegated implementing partner is required')

    def test_delegated_implementing_partner_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'delegated_implementing_partner',
                                 'delegated implementing partner is required')

    def test_start_date_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'start_date', 'delegation start_date is required')

    def test_end_date_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'end_date', 'delegation end_date is required')

    def test_financial_year_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'financial_year', 'financial year is required')

    def test_delegation_start_date_less_than_end_date(self):
        afya_jijini = ImplementingPartner.objects.get(pk=1)
        afya_ziwani = ImplementingPartner.objects.get(pk=2)
        five_weeks_ago = datetime.now() - timedelta(weeks=5)
        five_weeks_to_come = datetime.now() + timedelta(weeks=5)
        user = User.objects.first()

        self.assertModelClean(ServiceDelegation, {'start_date': five_weeks_ago,
                                                  'end_date': five_weeks_to_come},
                              'Delegation start date is less than delegation end date')

        self.assertModelNotClean(ServiceDelegation, {'start_date': five_weeks_to_come,
                                                     'end_date': five_weeks_ago,
                                                     'main_implementing_partner': afya_jijini,
                                                     'delegated_implementing_partner': afya_ziwani,
                                                     'created_by': user,
                                                     'updated_by': user,
                                                     'intervention_type': InterventionType.objects.first()},
                                 {'start_date'},
                                 'Delegation start date is less than delegation end date')
