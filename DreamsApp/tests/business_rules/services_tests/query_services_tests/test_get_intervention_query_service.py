from DreamsApp.business_rules.services.query_services.intervention_query_service import InterventionQueryService
from DreamsApp.models import Intervention
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class GetInterventionQueryServiceTestCase(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_y_user = test_data['ip_y_user']
        intervention = test_data['intervention_by_ip_z_to_ip_z_client_1']
        query_service = InterventionQueryService(user=ip_y_user)

        with self.assertRaises(Intervention.DoesNotExist, msg='Expected not to find the intervention'):
            query_service.get_intervention(intervention.id)

    def test_when_intervention_is_voided(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_y_user = test_data['ip_y_user']
        voided_intervention = test_data['voided_intervention_by_ip_y_to_ip_y_client_1']
        query_service = InterventionQueryService(user=ip_y_user)

        with self.assertRaises(Intervention.DoesNotExist, msg='Expected not to find the intervention'):
            query_service.get_intervention(voided_intervention.id)

    def test_when_intervention_belongs_to_user_ip(self):
        test_data = self.create_test_data_for_ip_clients()
        ip_z_user = test_data['ip_z_user']
        intervention = test_data['intervention_by_ip_z_to_ip_z_client_1']
        query_service = InterventionQueryService(user=ip_z_user)
        queried_intervention = query_service.get_intervention(intervention.id)
        self.assertEquals(intervention, queried_intervention,
                          'Expected queried intervention to equal intervention')

        intervention = test_data['intervention_by_ip_z_to_ip_y_client_1']
        query_service = InterventionQueryService(user=ip_z_user)
        expected_intervention = query_service.get_intervention(intervention.id)
        self.assertEquals(intervention, expected_intervention,
                          'Expected queried intervention to equal intervention')

    def test_when_user_ip_has_active_delegation_from_client_ip(self):
        test_data = self.create_test_data_for_ip_clients()

        self.create_delegation(delegating_implementing_partner=test_data['ip_y'],
                               delegated_implementing_partner=test_data['ip_x'])
        intervention = test_data['intervention_1_by_ip_y_to_ip_y_client_1']
        ip_x_user = test_data['ip_x_user']
        query_service = InterventionQueryService(user=ip_x_user)
        expected_intervention = query_service.get_intervention(intervention.id)
        self.assertEquals(intervention, expected_intervention,
                          'Expected queried intervention to equal intervention')
