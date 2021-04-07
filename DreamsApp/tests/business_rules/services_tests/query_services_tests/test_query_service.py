from DreamsApp.business_rules.services.query_services.client_query_service import ClientQueryService
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class GetClientsTestCase(InterventionDelegationTestCase):

    def test_returns_all_clients_who_belong_to_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_user = test_data['ip_x_user']
        query_service = ClientQueryService(user=ip_user)
        clients = query_service.get_clients()
        self.assertEquals(clients.count(), 3, 'Expected 3 clients that belong to the IP')

    def test_returns_all_clients_who_belong_to_user_and_delegating_ips(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_user = test_data['ip_x_user']
        main_implementing_partner = self.test_data['ip_x']
        delegated_implementing_partner = self.test_data['ip_y']

        self.create_active_delegation(delegating_implementing_partner=main_implementing_partner,
                                      delegated_implementing_partner=delegated_implementing_partner)
        query_service = ClientQueryService(user=ip_user)

        clients = query_service.get_clients(implementing_partner=ip_user)
        self.assertEquals(clients.count(), 5)

    def test_when_clients_from_other_ips_have_intervention_from_user_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_user = test_data['ip_y_user']
        query_service = ClientQueryService(user=ip_user)

        clients = query_service.get_clients(implementing_partner=ip_user)
        self.assertEquals(clients.count(), 4)
