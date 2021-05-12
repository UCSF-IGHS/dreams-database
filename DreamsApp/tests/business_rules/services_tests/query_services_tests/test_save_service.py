from DreamsApp.exceptions import DreamsBusinessRuleViolationException
from django.test import Client as TestClient
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class SaveTestCase(InterventionDelegationTestCase):

    def test_intervention_pre_save(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_user = test_data['ip_x_user']
        ip_user.user.set_password('12345')
        ip_user.user.save()

        client = TestClient()
        logged_in = client.login(username=ip_user.user.username, password='12345')


        intervention = test_data['intervention_by_ip_z_to_ip_y_client_2']
        with self.assertRaises(DreamsBusinessRuleViolationException):
            intervention.save()
