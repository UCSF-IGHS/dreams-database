from DreamsApp.business_rules.services.intervention_security_service import InterventionSecurityService
from DreamsApp.exceptions import InterventionNotWithinUserRealmBusinessRuleException
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class RuleCanDeleteInterventionTestCase(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        with self.assertRaises(InterventionNotWithinUserRealmBusinessRuleException):
            intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
            other_ip_user = self.ip_b_user
            InterventionSecurityService.rule_try_can_delete_intervention(other_ip_user,
                                                                         intervention_by_client_ip)

        with self.assertRaises(InterventionNotWithinUserRealmBusinessRuleException):
            intervention_by_second_random_ip = self.test_data['random_intervention']
            first_random_ip_user = self.test_data['random_ip_user']
            InterventionSecurityService.rule_try_can_delete_intervention(first_random_ip_user,
                                                                         intervention_by_second_random_ip)

    def test_when_intervention_belongs_to_user_ip(self):
        intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
        client_ip_user = self.ip_a_user
        checks_passed = InterventionSecurityService.rule_try_can_delete_intervention(client_ip_user,
                                                                                     intervention_by_client_ip)
        self.assertIn('VI003', checks_passed, 'Expected check VI003_intervention_belongs_to_user_ip to have passed')
