from __future__ import unicode_literals
from DreamsApp.models import *
from django.test import TestCase


class TestExternalOrganisationOtherTestCase(TestCase):
    def setUp(self):
        self.EXTERNAL_ORGANISATION = ExternalOrganisation.objects.get(pk=1) # fixture run by migration
        self.EXTERNAL_ORGANISATION_OTHER = "Global Communities"

    def tearDown(self):
        del self.EXTERNAL_ORGANISATION
        del self.EXTERNAL_ORGANISATION_OTHER

    def test_external_organisation_and_external_organisation_both_selected(self):
        external_organisation_and_external_organisation_both_selected = {
            "external_organisation": self.EXTERNAL_ORGANISATION ,
            "external_organisation_other": self.EXTERNAL_ORGANISATION_OTHER,
        }
        self.assertModelNotClean(Intervention, external_organisation_and_external_organisation_both_selected,
                              {'external_organisation_other'},
                              'external organisation and external_organisation_other cannot be both selected')
