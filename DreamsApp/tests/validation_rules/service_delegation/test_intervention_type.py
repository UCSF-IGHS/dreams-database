from __future__ import unicode_literals
from DreamsApp.models import ServiceDelegation, InterventionType
from xf.xf_system.tests.test_xf_test_case import XFTestCase


class TestInterventionTypeTestCase(XFTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_intervention_type_is_required(self):
        self.assertFieldRequired(ServiceDelegation, 'intervention_type', 'intervention type is required')