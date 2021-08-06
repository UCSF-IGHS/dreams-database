from DreamsApp.business_rules.services.enrolment_security_service import EnrolmentSecurityService
from DreamsApp.exceptions import EnrolmentNotWithinUserRealmBusinessRuleException
#from DreamsApp.tests.business_rules.services_tests.intervention_delegation_test_case import \
#

class RuleCanEditEnrolmentTestCase(): #(InterventionDelegationTestCase):

    def test_default_not_allowed(self):
        with self.assertRaises(EnrolmentNotWithinUserRealmBusinessRuleException):
            enrolment_by_client_ip = self.test_data['ip_b_client']
            non_client_ip_user = self.ip_a_user
            EnrolmentSecurityService.rule_try_can_edit_enrolment(non_client_ip_user,
                                                                 enrolment_by_client_ip)

        with self.assertRaises(EnrolmentNotWithinUserRealmBusinessRuleException):
            random_ip_user = self.test_data['random_ip_user']
            random_ip_enrolment = self.test_data['second_random_ip_client']
            EnrolmentSecurityService.rule_try_can_edit_enrolment(random_ip_user,
                                                                 random_ip_enrolment)

    def test_when_enrolment_belongs_to_user_ip(self):
        enrolment_by_client_ip = self.test_data['ip_a_client']
        client_ip_user = self.ip_a_user
        checks_passed = EnrolmentSecurityService.rule_try_can_edit_enrolment(client_ip_user,
                                                                             enrolment_by_client_ip)
        self.assertIn('C001', checks_passed, 'Expected check C001_client_belongs_to_ip to have passed')
