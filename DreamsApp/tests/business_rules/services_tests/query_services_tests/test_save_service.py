from DreamsApp.exceptions import DreamsBusinessRuleViolationException
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class SaveTestCase(InterventionDelegationTestCase):

    def test_intervention_pre_save_throws_exception_when_checks_failed(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_user = test_data['ip_x_user']
        request = self.setup_request(self._generate_dummy_request(ip_user.user), ip_user.user)
        intervention = test_data['intervention_by_ip_z_to_ip_y_client_2']

        with self.assertRaises(DreamsBusinessRuleViolationException):
            intervention.save()

    def test_intervention_pre_save_updates_intervention_when_checks_passed(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_user = test_data['ip_z_user']
        dummy_request = self._generate_dummy_request(ip_user.user)
        request = self.setup_request(dummy_request, ip_user.user)
        intervention = test_data['intervention_by_ip_z_to_ip_z_client_2']
        intervention.voided = True
        intervention.save()
        self.assertTrue(intervention.voided)


    def test_client_pre_save_throws_exception_when_checks_failed(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_user = test_data['ip_x_user']
        request = self.setup_request(self._generate_dummy_request(ip_user.user), ip_user.user)
        client = test_data['client_y_1']

        with self.assertRaises(DreamsBusinessRuleViolationException):
            client.save()

    def test_intervention_pre_save_updates_intervention_when_checks_passed(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_user = test_data['ip_x_user']
        request = self.setup_request(self._generate_dummy_request(ip_user.user), ip_user.user)
        client = test_data['client_x_1']
        client.voided = True
        client.save()
        self.assertTrue(client.voided)
