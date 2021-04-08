from DreamsApp.business_rules.services.query_services.client_query_service import ClientQueryService
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class GetClientsTestCase(InterventionDelegationTestCase):

    def test_when_clients_belong_to_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']
        query_service = ClientQueryService(user=user)
        clients = query_service.get_clients()
        self.assertEquals(clients.count(), 3, 'Expected 3 clients that belong to the IP')

    def test_when_user_ip_has_active_delegation(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']

        self.create_active_delegation(delegating_implementing_partner=test_data['ip_x'],
                                      delegated_implementing_partner=test_data['ip_y'])
        query_service = ClientQueryService(user=user)

        clients = query_service.get_clients()
        self.assertEquals(clients.count(), 6, 'Expected 6 clients that belong to user ip and delegating ip')

    def test_when_client_has_at_least_one_intervention(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_z_user']
        query_service = ClientQueryService(user=user)

        clients = query_service.get_clients()
        self.assertEquals(clients.count(), 5, 'Expected 5 clients: 3 from user ip, 2 from other ip with interventions')
