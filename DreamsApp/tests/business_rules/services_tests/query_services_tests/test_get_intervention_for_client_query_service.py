from DreamsApp.business_rules.services.query_services.intervention_query_service import InterventionQueryService
from DreamsApp.models import Intervention
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class GetInterventionForClientQueryServiceTestCase(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        client = test_data['client_x_1']
        query_service = InterventionQueryService(user=user)

        with self.assertRaises(Intervention.DoesNotExist):
            query_service.get_interventions_for_client(client=client)

    def test_when_client_belongs_to_user_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        client = test_data['client_y_1']
        query_service = InterventionQueryService(user=user)
        interventions = query_service.get_interventions_for_client(client = client)
        self.assertEquals(interventions.count(), 2, 'Expected 2 inteventions that belong to the IP')

        for intervention in interventions:
            self.assertEquals(intervention.client, client, 'Expected the intervention to belong to client {}'.format((client)))
            self.assertFalse(intervention.voided, 'Expected an unvoided intervention')

    def test_when_user_ip_has_active_delegation_from_client_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_x_user']

        self.create_delegation(delegating_implementing_partner=test_data['ip_y'],
                               delegated_implementing_partner=test_data['ip_x'])
        self.create_delegation(delegating_implementing_partner=test_data['ip_z'],
                               delegated_implementing_partner=test_data['ip_y'], active=False)
        client = test_data['client_y_1']
        query_service = InterventionQueryService(user=user)
        interventions = query_service.get_interventions_for_client(client=client)
        self.assertEquals(interventions.count(), 2, 'Expected 2 inteventions that belong to the IP')

        for intervention in interventions:
            self.assertEquals(intervention.client, client,
                              'Expected the intervention to belong to client {}'.format((client)))
            self.assertFalse(intervention.voided, 'Expected an unvoided intervention')
