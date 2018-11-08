from __future__ import unicode_literals
from DreamsApp.models import *
from DreamsApp.xf_test_case.xf_test_case import XFTestCase


class TestClientTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_client_is_required(self):
        self.assertFieldRequired(Intervention, 'client', 'client is required')
