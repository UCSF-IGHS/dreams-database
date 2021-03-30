from DreamsApp.business_rules.services.intervention_security_service import InterventionSecurityService
from DreamsApp.exceptions import InterventionNotWithinUserRealmBusinessRuleException
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class RuleCanViewInterventionTestCase(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        intervention_by_random_user = self.test_data['intervention_by_ip_b_to_ip_b_client']
        current_user = self.ip_a_user

        with self.assertRaises(InterventionNotWithinUserRealmBusinessRuleException):
            InterventionSecurityService.rule_try_can_view_intervention(current_user,
                                                                       intervention_by_random_user)
    def test_when_client_belongs_to_user_ip(self):
        intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
        client_ip_user = self.ip_a_user
        checks_passed = InterventionSecurityService.rule_try_can_view_intervention(client_ip_user,
                                                                                   intervention_by_client_ip)
        self.assertIn('VI002', checks_passed, 'Expected check v002_client_belongs_to_ip to have passed')

    def test_when_user_belongs_to_non_delegated_ip(self):
        intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
        non_delegated_ip_ip_user = self.ip_b_user
        with self.assertRaises(InterventionNotWithinUserRealmBusinessRuleException):
            InterventionSecurityService.rule_try_can_view_intervention(non_delegated_ip_ip_user,
                                                                                   intervention_by_client_ip)

    def test_when_intervention_belongs_to_user_ip(self):
        intervention = self.test_data['intervention_by_ip_b_to_ip_a_client']
        client_ip_user = self.ip_b_user
        checks_passed = InterventionSecurityService.rule_try_can_view_intervention(client_ip_user,
                                                                                   intervention)
        self.assertIn('VI003', checks_passed, 'Expected check VI003_intervention_belongs_to_user_ip to have passed')

    def test_when_user_ip_has_active_delegation_from_client_ip(self):
        intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
        delegated_ip_user = self.ip_b_user
        self.delegate_intervention_1003(delegating_implementing_partner=self.ip_a,
                                        delegated_implementing_partner=self.ip_b)
        checks_passed = InterventionSecurityService.rule_try_can_view_intervention(delegated_ip_user,
                                                                                   intervention_by_client_ip)
        self.assertIn('VI004', checks_passed, 'Expected check VI004_ip_has_active_delegation to have passed')
