from DreamsApp.business_rules.services.intervention_security_service import InterventionSecurityService
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class RuleCanAddInterventionTestCase(InterventionDelegationTestCase):

    def test_when_client_belongs_to_user_ip(self):
        intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
        client_ip_user = self.ip_a_user
        checks_passed = InterventionSecurityService.rule_try_can_view_intervention(client_ip_user,
                                                                                   intervention_by_client_ip)
        self.assertIn('VI002', checks_passed, 'Expected check v002_client_belongs_to_ip to have passed')

    def test_when_user_ip_has_active_delegation_from_client_ip(self):
        intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
        delegated_ip_user = self.ip_b_user
        self.delegate_intervention_1003(delegating_implementing_partner=self.ip_a,
                                        delegated_implementing_partner=self.ip_b)
        checks_passed = InterventionSecurityService.rule_try_can_add_intervention(delegated_ip_user,
                                                                                  intervention_by_client_ip)
        self.assertIn('VI004', checks_passed, 'Expected check VI004_ip_has_active_delegation to have passed')
