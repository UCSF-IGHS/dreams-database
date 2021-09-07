from __future__ import unicode_literals
from DreamsApp.models import *
from django.test import TestCase


class TestClientTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_client_is_required(self):
        self.assertFieldRequired(Intervention, 'client', 'client is required')
