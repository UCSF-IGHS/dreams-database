from DreamsApp.business_rules.services.intervention_security_service import InterventionSecurityService
from DreamsApp.exceptions import InterventionNotWithinUserRealmBusinessRuleException
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class RuleCanAddInterventionTestCase(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        intervention_for_random_ip_client = self.test_data['intervention_by_ip_b_to_ip_b_client']
        current_user = self.ip_a_user

        with self.assertRaises(InterventionNotWithinUserRealmBusinessRuleException):
            InterventionSecurityService.rule_try_can_add_intervention(current_user,
                                                                      intervention_for_random_ip_client)

    def test_when_client_belongs_to_user_ip(self):
        intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
        client_ip_user = self.ip_a_user
        checks_passed = InterventionSecurityService.rule_try_can_add_intervention(client_ip_user,
                                                                                  intervention_by_client_ip)
        self.assertIn('VI002', checks_passed, 'Expected check vi002_client_belongs_to_ip to have passed')

    def test_when_user_ip_has_active_delegation_from_client_ip(self):
        intervention_by_client_ip = self.test_data['intervention_by_ip_a_to_ip_a_client']
        delegated_ip_user = self.ip_b_user
        self.create_delegation(delegating_implementing_partner=self.ip_a,
                               delegated_implementing_partner=self.ip_b)
        checks_passed = InterventionSecurityService.rule_try_can_add_intervention(delegated_ip_user,
                                                                                  intervention_by_client_ip)
        self.assertIn('VI004', checks_passed, 'Expected check VI004_ip_has_active_delegation to have passed')


    def test_when_a_pending_referral_from_user_ip_to_client_ip(self):
        test_data=self.generate_test_data()
        intervention_to_non_delegating_ip_client = self.test_data['intervention_by_ip_b_to_ip_a_client']
        referral = self.create_referral(test_data['ip_a_client'], test_data['ip_a'], test_data['ip_b'])
        intervention_to_non_delegating_ip_client.client = referral.client
        intervention_to_non_delegating_ip_client.save()
        receiving_ip_user = self.test_data['ip_b_user']

        checks_passed = InterventionSecurityService.rule_try_can_add_intervention(receiving_ip_user,
                                                                                  intervention_to_non_delegating_ip_client)
        self.assertIn('VI005', checks_passed, 'Expected check VI005_check_client_has_active_referral_to_ip'
                                              ' to have passed')

