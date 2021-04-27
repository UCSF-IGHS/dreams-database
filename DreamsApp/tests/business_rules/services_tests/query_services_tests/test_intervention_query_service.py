from DreamsApp.business_rules.services.query_services.intervention_query_service import InterventionQueryService
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class InterventionQueryServiceTestCase(InterventionDelegationTestCase):

    def test_when_interventions_belong_to_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_z_user']
        query_service = InterventionQueryService(user=user)
        interventions = query_service.get_interventions()
        self.assertEquals(interventions.count(), 5, 'Expected 5 inteventions that belong to the IP')

        for intervention in interventions:
            self.assertEquals(intervention.implementing_partner, test_data['ip_z'], 'Expected the intervention ip to be ip_z')
            self.assertFalse(intervention.voided, 'Expected an unvoided intervention')

    def test_when_client_with_interventions_belongs_to_user_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        query_service = InterventionQueryService(user=user)
        interventions = query_service.get_interventions()
        self.assertEquals(interventions.count(), 3, 'Expected 2 inteventions for clients who belong to IP')

        for intervention in interventions:
            self.assertEquals(intervention.client.implementing_partner, test_data['ip_y'], 'Expected the client ip to be ip_y')
            self.assertFalse(intervention.voided, 'Expected an unvoided intervention')

    def test_when_user_ip_has_active_delegation(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']

        self.create_delegation(delegating_implementing_partner=test_data['ip_x'],
                               delegated_implementing_partner=test_data['ip_y'])
        self.create_delegation(delegating_implementing_partner=test_data['ip_z'],
                               delegated_implementing_partner=test_data['ip_y'], active=False)
        query_service = InterventionQueryService(user=user)
        interventions = query_service.get_interventions()

        self.assertEquals(interventions.count(), 5,
                          'Expected interventions: that belong to user ip(3) and IP with active delegation(2)')

        ipx_interventions = interventions.filter(client__implementing_partner=test_data['ip_x'])
        self.assertEquals(ipx_interventions.count(), 2, 'Expected 2 interventions from ip_x')

        ipy_interventions = interventions.filter(client__implementing_partner=test_data['ip_y'])
        self.assertEquals(ipy_interventions.count(), 3, 'Expected 3 interventions from ip_y')

        for intervention in interventions:
            self.assertFalse(intervention.voided, 'Expected an unvoided intervention')
