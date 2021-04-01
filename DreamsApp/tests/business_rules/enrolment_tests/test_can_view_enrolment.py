from DreamsApp.business_rules.services.enrolment_security_service import EnrolmentSecurityService
from DreamsApp.exceptions import EnrolmentNotWithinUserRealmBusinessRuleException
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class RuleCanViewEnrolmentTestCase(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        random_client = self.test_data['ip_b_client']
        current_user = self.ip_a_user

        with self.assertRaises(EnrolmentNotWithinUserRealmBusinessRuleException):
            EnrolmentSecurityService.rule_try_can_view_enrolment(current_user,
                                                                 random_client)

    def test_when_client_belongs_to_user_ip(self):
        enrolment_by_client_ip = self.test_data['ip_a_client']
        client_ip_user = self.ip_a_user
        checks_passed = EnrolmentSecurityService.rule_try_can_view_enrolment(client_ip_user,
                                                                             enrolment_by_client_ip)
        self.assertIn('C001', checks_passed, 'Expected check C001_client_belongs_to_ip to have passed')

    def test_when_user_ip_has_active_delegation_from_client_ip(self):
        enrolment_by_client_ip = self.test_data['ip_a_client']
        delegated_ip_user = self.ip_b_user
        self.create_active_delegation(delegating_implementing_partner=self.ip_a,
                                      delegated_implementing_partner=self.ip_b)
        checks_passed = EnrolmentSecurityService.rule_try_can_view_enrolment(delegated_ip_user,
                                                                             enrolment_by_client_ip)
        self.assertIn('C002', checks_passed, 'Expected check COO2_ip_has_active_delegation to have passed')
