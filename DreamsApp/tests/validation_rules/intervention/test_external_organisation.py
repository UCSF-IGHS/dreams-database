from __future__ import unicode_literals
from DreamsApp.models import *
from django.test import TestCase


class TestExternalOrganisationTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_external_organisation_is_optional(self):
        self.assertFieldOptional(Intervention, 'external_organisation', 'external_organisation is optional')
