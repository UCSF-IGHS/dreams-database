from DreamsApp.business_rules.services.query_services.intervention_query_service import InterventionQueryService
from DreamsApp.models import Intervention
#from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
#    InterventionDelegationTestCase


class GetInterventionsForClientQueryServiceTestCase(): #(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        client = test_data['client_x_1']
        query_service = InterventionQueryService(user=user)

        with self.assertRaises(Intervention.DoesNotExist, msg='Expected not to find the intervention'):
            query_service.get_interventions_for_client(client)

    def test_when_client_belongs_to_user_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        client = test_data['client_y_1']
        query_service = InterventionQueryService(user=user)
        interventions = query_service.get_interventions_for_client(client)
        self.assertEquals(interventions.count(), 4, 'Expected 4 interventions that belong to client_y_1')

        for intervention in interventions:
            self.assertEquals(intervention.client, client,
                              'Expected the intervention to belong to client {}'.format((client)))
            self.assertFalse(intervention.voided, 'Expected an unvoided intervention')
    """
    def test_when_user_ip_has_active_delegation_from_client_ip(self):
        test_data = self.create_test_data_for_ip_clients()

        self.create_delegation(delegating_implementing_partner=test_data['ip_y'],
                               delegated_implementing_partner=test_data['ip_x'])
        client = test_data['client_y_1']
        user = test_data['ip_x_user']
        query_service = InterventionQueryService(user=user)
        interventions = query_service.get_interventions_for_client(client)
        self.assertEquals(interventions.count(), 4, 'Expected 3 inteventions, 2 from ip_x, 1 from ip_y, 1 from ip_z')

        for intervention in interventions:
            self.assertEquals(intervention.client, client,
                              'Expected the intervention to belong to client {}'.format((client)))
            self.assertFalse(intervention.voided, 'Expected an unvoided intervention')
    """
    def test_when_user_ip_has_intervention_for_client(self):
        test_data = self.create_test_data_for_ip_clients()
        client = test_data['client_y_1']
        user = test_data['ip_x_user']
        query_service = InterventionQueryService(user=user)
        interventions = query_service.get_interventions_for_client(client)
        self.assertEquals(interventions.count(), 1, 'Expected 1 intevention, only interventions received from ip_x')

        for intervention in interventions:
            self.assertEquals(intervention.client, client,
                              'Expected the intervention to belong to client {}'.format((client)))
            self.assertFalse(intervention.voided, 'Expected an unvoided intervention')
