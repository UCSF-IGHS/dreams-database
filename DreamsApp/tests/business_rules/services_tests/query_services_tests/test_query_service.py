from DreamsApp.business_rules.services.query_services.client_query_service import ClientQueryService
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class GetClientsTestCase(InterventionDelegationTestCase):

    def test_when_clients_belong_to_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        query_service = ClientQueryService(user=user)
        clients = query_service.get_clients()
        self.assertEquals(clients.count(), 4, 'Expected 4 clients that belong to the IP')

        for client in clients:
            self.assertEquals(client.implementing_partner, test_data['ip_y'], 'Expected the client ip to be ip_y')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_when_user_ip_has_active_delegation(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']

        self.create_delegation(delegating_implementing_partner=test_data['ip_x'],
                               delegated_implementing_partner=test_data['ip_y'])
        self.create_delegation(delegating_implementing_partner=test_data['ip_z'],
                               delegated_implementing_partner=test_data['ip_y'], active=False)
        query_service = ClientQueryService(user=user)

        clients = query_service.get_clients()
        self.assertEquals(clients.count(), 7,
                          'Expected 7 clients that belong to user ip(4) and IP with active delegation(3)')
        for client in clients:
            self.assertIn(client.implementing_partner, [test_data['ip_x'], test_data['ip_y']],
                          'Expected the client ip to be either ip_x or ip_y')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_when_client_has_at_least_one_intervention(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_z_user']
        query_service = ClientQueryService(user=user)

        clients = query_service.get_clients()
        self.assertEquals(clients.count(), 5, 'Expected 5 clients: 3 from user IP Z, 2 from IP Y')

        ip_y, ip_z = test_data["ip_y"], test_data["ip_z"]

        for client in clients:
            self.assertTrue(client.implementing_partner == ip_z or (
                    client.get_full_name() == 'Client Y   One' or client.get_full_name() == 'Client Y Doe 2'))
            self.assertFalse(client.voided, 'Expected a client who is not voided')

        for client in clients:
            if client.get_full_name() == 'Client Y   One':
                self.assertEquals(client.implementing_partner, test_data["ip_y"])

            elif client.get_full_name() == 'Client Y Doe 2':
                self.assertEquals(client.implementing_partner, test_data["ip_y"])

            elif client.get_full_name() == 'ClientZ   One':
                self.assertEquals(client.implementing_partner, test_data["ip_z"])

            elif client.get_full_name() == 'Client Z   2':
                self.assertEquals(client.implementing_partner, test_data["ip_z"])

            elif client.get_full_name() == 'Client Z   3':
                self.assertEquals(client.implementing_partner, test_data["ip_z"])

            else:
                raise AssertionError('Client not expected in the list')
