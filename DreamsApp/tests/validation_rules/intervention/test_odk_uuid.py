
from __future__ import unicode_literals
from DreamsApp.models import *
from xf.xf_system.tests.test_xf_test_case import XFTestCase


class TestODKUUID(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_external_organisation_other_is_optional(self):
        self.assertFieldOptional(Intervention, 'odk_uuid', 'odk uuid is optional')
