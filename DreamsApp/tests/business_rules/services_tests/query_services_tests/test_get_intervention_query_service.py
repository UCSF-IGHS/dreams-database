from DreamsApp.business_rules.services.query_services.intervention_query_service import InterventionQueryService
from DreamsApp.models import Intervention
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class GetInterventionQueryServiceTestCase(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_y_user']
        intervention = test_data['intervention_1_by_ip_z_to_ip_z_client_1']
        query_service = InterventionQueryService(user=user)

        with self.assertRaises(Intervention.DoesNotExist, msg='Expected not to find the intervention'):
            query_service.get_intervention(intervention.id)

    def test_when_intervention_belongs_to_user_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        user = test_data['ip_z_user']
        intervention_1_by_ip_z_to_ip_z_client_1 = test_data['intervention_1_by_ip_z_to_ip_z_client_1']
        query_service = InterventionQueryService(user=user)
        queried_intervention = query_service.get_intervention(intervention_1_by_ip_z_to_ip_z_client_1.id)
        self.assertEquals(intervention_1_by_ip_z_to_ip_z_client_1, queried_intervention,
                          'Expected queried intervention to equal intervention')

        intervention_by_ip_z_to_ip_y_client_1 = test_data['intervention_by_ip_z_to_ip_y_client_1']
        query_service = InterventionQueryService(user=user)
        expected_intervention = query_service.get_intervention(intervention_by_ip_z_to_ip_y_client_1.id)
        self.assertEquals(intervention_by_ip_z_to_ip_y_client_1, expected_intervention,
                          'Expected queried intervention to equal intervention')

    def test_when_user_ip_has_active_delegation_from_client_ip(self):
        test_data = self.create_test_data_for_ip_clients()

        self.create_delegation(delegating_implementing_partner=test_data['ip_y'],
                               delegated_implementing_partner=test_data['ip_x'])
        intervention_1_by_ip_y_to_ip_y_client_1 = test_data['intervention_1_by_ip_y_to_ip_y_client_1']
        user = test_data['ip_x_user']
        query_service = InterventionQueryService(user=user)
        expected_intervention = query_service.get_intervention(intervention_1_by_ip_y_to_ip_y_client_1.id)
        self.assertEquals(intervention_1_by_ip_y_to_ip_y_client_1, expected_intervention,
                          'Expected queried intervention to equal intervention')
