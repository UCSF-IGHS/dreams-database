from __future__ import unicode_literals
from DreamsApp.models import *
from django.test import TestCase


class TestExternalOrganisationOtherTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_external_organisation_other_is_optional(self):
        self.assertFieldOptional(Intervention, 'external_organisation_other', 'external_organisation_other is optional')
