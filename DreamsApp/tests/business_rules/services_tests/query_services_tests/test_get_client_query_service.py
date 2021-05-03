from DreamsApp.business_rules.services.query_services.client_query_service import ClientQueryService
from DreamsApp.models import Client
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class GetClientTestCase(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']
        query_service = ClientQueryService(user=user)
        dreams_id = '102/1232/1'

        with self.assertRaises(Client.DoesNotExist):
            query_service.get_client(dreams_id)

    def test_when_clients_belong_to_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']
        query_service = ClientQueryService(user=user)
        client = query_service.get_client(dreams_id='100/1232/1')
        self.assertEquals(client.dreams_id, '100/1232/1', 'Expected client have dreams id 100/1232/1')
        self.assertEquals(client.implementing_partner, test_data['ip_x'], 'Expected ip to be IP X')
        self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_when_user_ip_has_active_delegation(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']

        self.create_delegation(delegating_implementing_partner=test_data['ip_x'],
                               delegated_implementing_partner=test_data['ip_y'])
        query_service = ClientQueryService(user=user)

        client = query_service.get_client(dreams_id='100/1232/1')
        self.assertEquals(client.dreams_id, '100/1232/1', 'Expected client have dreams id 100/1232/1')
        self.assertEquals(client.implementing_partner, test_data['ip_x'], 'Expected ip to be IP X')
        self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_when_client_has_at_least_one_intervention(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_z_user']
        query_service = ClientQueryService(user=user)
        client = query_service.get_client(dreams_id='101/1232/1')

        self.assertEquals(client.dreams_id, '101/1232/1', 'Expected client have dreams id 101/1232/1')
        self.assertEquals(client.implementing_partner, test_data['ip_y'], 'Expected ip to be IP Y')
        self.assertFalse(client.voided, 'Expected a client who is not voided')
