from DreamsApp.business_rules.check_rules.enrolment_security_service_checks import EnrolmentSecurityServiceChecks
from DreamsApp.exceptions import EnrolmentNotWithinUserRealmBusinessRuleException

class EnrolmentSecurityService:

    @classmethod
    def rule_try_can_view_enrolment(cls, user , enrolment):
        checks_passed = []
        c001 = EnrolmentSecurityServiceChecks.check_client_belongs_to_ip(enrolment, user.implementing_partner)
        if c001 is None:
            c002 = EnrolmentSecurityServiceChecks.check_ip_has_active_delegation(
                    enrolment.implementing_partner, user.implementing_partner)
            if c002 is not None:
                checks_passed.append(c002)
        else:
            checks_passed.append(c001)

        if checks_passed:
            return checks_passed
        else:
            raise EnrolmentNotWithinUserRealmBusinessRuleException