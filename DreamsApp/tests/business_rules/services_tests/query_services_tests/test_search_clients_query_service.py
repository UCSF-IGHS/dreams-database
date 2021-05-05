from datetime import datetime, timedelta

from DreamsApp.business_rules.services.query_services.client_query_service import ClientQueryService
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class SearchClientTestCase(InterventionDelegationTestCase):

    def test_search_by_enrolment_date(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']
        query_service = ClientQueryService(user=user)
        search_criteria = {'enrolment_start_date': datetime.now() - timedelta(weeks=59),
                           'enrolment_end_date': datetime.now()}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 2, 'Expected 2 client created within the specified date range')

        for client in clients:
            self.assertTrue(clients.enrollment_date >= search_criteria['enrolment_start_date'],
                            msg='Expected first name if client to be Client X')
            self.assertTrue(clients.enrollment_date <= search_criteria['enrolment_end_date'],
                            msg='Expected first name if client to be Client X')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_search_by_search_text_for_name(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        self.create_delegation(delegating_implementing_partner=test_data['ip_x'],
                               delegated_implementing_partner=test_data['ip_y'])
        query_service = ClientQueryService(user=user)

        search_criteria = {'search_text': 'Client X'}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 3, 'Expected 3 client whose first names are Client X')

        for client in clients:
            self.assertEquals(clients.first_name, 'Client X',
                              msg='Expected client first name to be Client X')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

        search_criteria = {'search_text': '1'}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 2, 'Expected 2 client whose last names are 1')

        for client in clients:
            self.assertEquals(clients.lastname, '1',
                              msg='Expected client last name to be 1')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

        search_criteria = {'search_text': 'Doe'}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 3, 'Expected 3 client whose middle names are Doe')

        for client in clients:
            self.assertEquals(clients.middle_name, 'Doe',
                              msg='Expected client middlename name to be Doe')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_search_by_search_text_for_dreams_id(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        self.create_delegation(delegating_implementing_partner=test_data['ip_x'],
                               delegated_implementing_partner=test_data['ip_y'])
        query_service = ClientQueryService(user=user)

        search_criteria = {'search_text': '100/1232/1'}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 1, 'Expected 1 client whose dreams ID is 100/1232/1')

        for client in clients:
            self.assertEquals(clients.dreams_id, '100/1232/1',
                              msg='Expected client dreams ID to be 100/1232/1')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_search_by_ward(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']
        query_service = ClientQueryService(user=user)
        ward = test_data['sub_county_x_1_ward_1']
        search_criteria = {'ward': ward}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 2, 'Expected 2 clients enrolled in ward sub_county_x_1_ward_1')

        for client in clients:
            self.assertTrue(clients.ward == ward, msg='Expected client ward to be {}'.format(ward))
            self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_search_by_sub_county(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']
        query_service = ClientQueryService(user=user)
        sub_county = test_data['sub_county_x_1']
        search_criteria = {'ward': sub_county}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 3, 'Expected 3 clients enrolled in sub county sub_county_x_1'.format(sub_county))

        for client in clients:
            self.assertTrue(clients.ward.sub_county == sub_county,
                            msg='Expected client sub-county to be sub_county_x_1')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_search_by_county(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        self.create_delegation(delegating_implementing_partner=test_data['ip_x'],
                               delegated_implementing_partner=test_data['ip_y'])
        query_service = ClientQueryService(user=user)
        county = test_data['county_y']
        search_criteria = {'ward': county}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 3, 'Expected 3 clients enrolled in county county_y')

        for client in clients:
            self.assertTrue(clients.ward.sub_county.county == county,
                            msg='Expected client county to be county_y')
            self.assertFalse(client.voided, 'Expected a client who is not voided')
