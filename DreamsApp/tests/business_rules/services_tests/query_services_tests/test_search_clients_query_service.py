from datetime import datetime, timedelta

from DreamsApp.business_rules.services.query_services.client_query_service import ClientQueryService
from DreamsApp.models import Client
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class SearchClientTestCase(InterventionDelegationTestCase):
    def test_no_result_raises_not_found(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']
        query_service = ClientQueryService(user=user)
        search_criteria = {'enrolment_start_date': datetime.now().date() - timedelta(days=1),
                           'enrolment_end_date': datetime.now().date()}
        with self.assertRaises(Client.DoesNotExist):
            query_service.search_clients(search_criteria)

        search_criteria = {'search_text': 'Missing Name'}
        with self.assertRaises(Client.DoesNotExist):
            query_service.search_clients(search_criteria)

    def test_search_by_enrolment_date(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']
        query_service = ClientQueryService(user=user)
        search_criteria = {'enrolment_start_date': datetime.now().date() - timedelta(weeks=57),
                           'enrolment_end_date': datetime.now().date()}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 2, 'Expected 2 client created within the specified date range')

        for client in clients:
            self.assertTrue(client.date_of_enrollment >= search_criteria['enrolment_start_date'],
                            msg='Expected first name if client to be Client X')
            self.assertTrue(client.date_of_enrollment <= search_criteria['enrolment_end_date'],
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

        search_criteria = {'search_text': 'One'}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 2, 'Expected 2 client whose last names are One')

        for client in clients:
            self.assertEquals(client.last_name, 'One',
                              msg='Expected client last name to be One')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

        search_criteria = {'search_text': 'Doe'}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 3, 'Expected 3 client whose middle names are Doe')

        for client in clients:
            self.assertEquals(client.middle_name, 'Doe',
                              msg='Expected client middlename name to be Doe')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

        search_criteria = {'search_text': 'Client X Doe'}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 2, 'Expected 2 client with First name Client X and middle name Doe')

        for client in clients:
            self.assertEquals(client.middle_name, 'Doe',
                              msg='Expected client middlename name to be Doe')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

        user = test_data['ip_z_user']
        query_service = ClientQueryService(user=user)
        search_criteria = {'search_text': 'ClientZ'}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 1, 'Expected 1 client whose last names are ClientZ')

        for client in clients:
            self.assertEquals(client.first_name, 'ClientZ',
                              msg='Expected client last name to be 1')
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
            self.assertEquals(client.dreams_id, '100/1232/1',
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
            self.assertTrue(client.ward == ward, msg='Expected client ward to be {}'.format(ward))
            self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_search_by_sub_county(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']
        query_service = ClientQueryService(user=user)
        sub_county = test_data['sub_county_x_1']
        search_criteria = {'sub_county': sub_county}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 3,
                          'Expected 3 clients enrolled in sub county sub_county_x_1'.format(sub_county))

        for client in clients:
            self.assertTrue(client.ward.sub_county == sub_county,
                            msg='Expected client sub-county to be sub_county_x_1')
            self.assertFalse(client.voided, 'Expected a client who is not voided')

    def test_search_by_county(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        self.create_delegation(delegating_implementing_partner=test_data['ip_x'],
                               delegated_implementing_partner=test_data['ip_y'])
        query_service = ClientQueryService(user=user)
        county = test_data['county_y']
        search_criteria = {'county': county}
        clients = query_service.search_clients(search_criteria)
        self.assertEquals(clients.count(), 3, 'Expected 3 clients enrolled in county county_y')

        for client in clients:
            self.assertTrue(client.ward.sub_county.county == county, msg='Expected client county to be county_y')
            self.assertFalse(client.voided, 'Expected a client who is not voided')
