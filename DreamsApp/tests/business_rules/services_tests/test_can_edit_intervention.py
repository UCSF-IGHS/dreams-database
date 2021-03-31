from DreamsApp.business_rules.services.intervention_security_service import InterventionSecurityService
from DreamsApp.exceptions import InterventionNotWithinUserRealmBusinessRuleException
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class RuleCanEditInterventionTestCase(InterventionDelegationTestCase):

    def test_when_intervention_belongs_to_user_ip(self):
        intervention = self.test_data['intervention_by_ip_a_to_ip_a_client']
        client_ip_user = self.ip_a_user
        checks_passed = InterventionSecurityService.rule_try_can_edit_intervention(client_ip_user,
                                                                                   intervention)
        self.assertIn('VI003', checks_passed, 'Expected check VI003_intervention_belongs_to_user_ip to have passed')

    def test_when_intervention_does_not_belongs_to_user_ip(self):
        intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
        another_ip_user = self.ip_b_user

        with self.assertRaises(InterventionNotWithinUserRealmBusinessRuleException):
            InterventionSecurityService.rule_try_can_edit_intervention(another_ip_user,
                                                                                       intervention_by_client_ip)
