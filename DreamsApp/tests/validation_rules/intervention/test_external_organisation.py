from __future__ import unicode_literals
from DreamsApp.models import *
from xf.xf_system.tests.test_xf_test_case import XFTestCase


class TestExternalOrganisationTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_external_organisation_is_optional(self):
        self.assertFieldOptional(Intervention, 'external_organisation', 'external_organisation is optional')
