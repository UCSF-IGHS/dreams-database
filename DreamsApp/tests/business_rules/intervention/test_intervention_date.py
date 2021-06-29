from __future__ import unicode_literals
from DreamsApp.models import *
import datetime
from xf.xf_system.tests.test_xf_test_case import XFTestCase


class TestInterventionDateTestCase(XFTestCase):
    # load fixtures
    fixtures = ['test_verification_document.json', 'test_intervention_category.json', 'test_intervention_type.json',
                'test_county.json',
                'test_sub_county.json', 'test_ward.json', 'test_marital_status.json', 'test_user.json',
                'external_organisation_type.json', 'external_organisation.json', 'implementing_partner_funder.json', 'test_implementing_partner.json', 'test_client.json',
                'test_hts_result.json', 'test_pregnancy_test_result.json', 'test_intervention.json']

    def setUp(self):
        self.CLIENT = Client.objects.get(pk=1) # 2017-9-10
        self.EXTERNAL_ORGANISATION = ExternalOrganisation.objects.get(pk=1)

    def tearDown(self):
        del self.CLIENT
        del self.EXTERNAL_ORGANISATION

    def test_less_than_enrolment_date_for_implementing_partner(self):
        intervention_date_less_than_enrolment_date_for_implementing_partner = {
            "intervention_date": datetime.datetime.strptime('2017-2-2', '%Y-%m-%d').date(),
            "client": self.CLIENT
        }
        self.assertModelNotClean(Intervention, intervention_date_less_than_enrolment_date_for_implementing_partner,
                              {'intervention_date'},
                              'intervention date cannot be earlier than enrolment date for implementing partner')

    def test_less_than_enrolment_date_for_external_organisation(self):
        intervention_date_less_than_enrolment_date_for_external_organisation = {
            "intervention_date": datetime.datetime.strptime('2017-2-2', '%Y-%m-%d').date(),
            "client": self.CLIENT,
            "external_organisation": self.EXTERNAL_ORGANISATION
        }
        self.assertModelClean(Intervention, intervention_date_less_than_enrolment_date_for_external_organisation,
                              {'intervention_date'},
                              'intervention date cannot be earlier than enrolment date for external organisation')

    def test_more_than_enrolment_date(self):
        intervention_date_more_than_enrolment_date = {
            "intervention_date": datetime.datetime.strptime('2017-11-11', '%Y-%m-%d').date(),
            "client": self.CLIENT,
        }
        self.assertModelClean(Intervention, intervention_date_more_than_enrolment_date,
                                 {'intervention_date'},
                                 'intervention date cannot be earlier than enrolment date')

    def test_more_equal_to_enrolment_date(self):
        intervention_date_equal_to_than_enrolment_date = {
            "intervention_date": datetime.datetime.strptime('2017-9-10', '%Y-%m-%d').date(),
            "client": self.CLIENT,
        }
        self.assertModelClean(Intervention, intervention_date_equal_to_than_enrolment_date,
                                 {'intervention_date'},
                                 'intervention date cannot be earlier than enrolment date')
