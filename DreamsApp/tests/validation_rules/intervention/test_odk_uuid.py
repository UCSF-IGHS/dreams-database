
from __future__ import unicode_literals
from DreamsApp.models import *
from django.test import TestCase


class TestODKUUID(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_odk_uuid_is_optional(self):
        self.assertFieldOptional(Intervention, 'odk_uuid', 'odk uuid is optional')
