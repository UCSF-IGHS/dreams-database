from DreamsApp.business_rules.services.enrolment_security_service import EnrolmentSecurityService
from DreamsApp.exceptions import EnrolmentNotWithinUserRealmBusinessRuleException
from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
    InterventionDelegationTestCase


class RuleCanEditEnrolmentTestCase(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        with self.assertRaises(EnrolmentNotWithinUserRealmBusinessRuleException):
            random_enrolment = self.test_data['ip_b_client']
            current_user = self.ip_a_user
            EnrolmentSecurityService.rule_try_can_edit_enrolment(current_user,
                                                                 random_enrolment)

        with self.assertRaises(EnrolmentNotWithinUserRealmBusinessRuleException):
            enrolment_by_user_ip = self.test_data['ip_a_client']
            another_ip_user = self.ip_b_user
            EnrolmentSecurityService.rule_try_can_edit_enrolment(another_ip_user,
                                                                    enrolment_by_user_ip)

    def test_when_enrolment_belongs_to_user_ip(self):
        enrolment_by_client_ip = self.test_data['ip_a_client']
        client_ip_user = self.ip_a_user
        checks_passed = EnrolmentSecurityService.rule_try_can_edit_enrolment(client_ip_user,
                                                                             enrolment_by_client_ip)
        self.assertIn('C001', checks_passed, 'Expected check C001_client_belongs_to_ip to have passed')
