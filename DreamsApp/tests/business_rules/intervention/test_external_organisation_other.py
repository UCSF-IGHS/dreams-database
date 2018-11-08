from __future__ import unicode_literals
from DreamsApp.models import *
import datetime
from DreamsApp.xf_test_case.xf_test_case import XFTestCase


class TestExternalOrganisationOtherTestCase(XFTestCase):
    # load fixtures
    fixtures = ['external_organisation_type.json', 'external_organisation.json']

    def setUp(self):
        self.EXTERNAL_ORGANISATION = ExternalOrganisation.objects.get(pk=4)
        self.EXTERNAL_ORGANISATION_OTHER = None

    def tearDown(self):
        del self.EXTERNAL_ORGANISATION
        self.EXTERNAL_ORGANISATION_OTHER

    def test_external_organisation_other_is_required_if_external_organisation_is_other(self):
        external_organisation_other_is_required_if_external_organisation_is_other = {
            "external_organisation": self.EXTERNAL_ORGANISATION,
            "external_organisation_other": None
        }
        self.assertModelNotClean(Intervention, external_organisation_other_is_required_if_external_organisation_is_other,
                              {'external_organisation_other'},
                              'External organisation other is required if external organisation is Other')
