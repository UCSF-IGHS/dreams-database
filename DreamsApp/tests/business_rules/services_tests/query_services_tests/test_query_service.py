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

        for client in clients:
            self.assertEquals(client.implementing_partner, test_data['ip_x'], 'Expected the client ip to be ip_x')

    def test_when_user_ip_has_active_delegation(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']

        self.create_active_delegation(delegating_implementing_partner=test_data['ip_x'],
                                      delegated_implementing_partner=test_data['ip_y'])
        query_service = ClientQueryService(user=user)

        clients = query_service.get_clients()
        self.assertEquals(clients.count(), 6, 'Expected 6 clients that belong to user ip and delegating ip')
        for client in clients:
            self.assertIn(client.implementing_partner, [test_data['ip_x'], test_data['ip_y']],
                          'Expected the client ip to be either ip_x or ip_y')

    def test_when_client_has_at_least_one_intervention(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_z_user']
        query_service = ClientQueryService(user=user)

        clients = query_service.get_clients()
        self.assertEquals(clients.count(), 5, 'Expected 5 clients: 3 from user IP Z, 2 from IP Y')

        clients.order_by('first_name', 'last_name')

        for client in clients:
            if client.first_name == 'Client Y' and client.last_name == '1':
                self.assertEquals(client.implementing_partner, test_data["ip_y"])

            elif client.first_name == 'Client Y' and client.last_name == '2':
                self.assertEquals(client.implementing_partner, test_data["ip_y"])

            elif client.first_name == 'Client Z' and client.last_name == '1':
                self.assertEquals(client.implementing_partner, test_data["ip_z"])

            elif client.first_name == 'Client Z' and client.last_name == '2':
                self.assertEquals(client.implementing_partner, test_data["ip_z"])

            elif client.first_name == 'Client Z' and client.last_name == '3':
                self.assertEquals(client.implementing_partner, test_data["ip_z"])

            else:
                raise AssertionError("This client was not expected in the result set")
