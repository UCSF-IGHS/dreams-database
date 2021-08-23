from DreamsApp.business_rules.check_rules.enrolment_security_service_checks import EnrolmentSecurityServiceChecks
from DreamsApp.exceptions import EnrolmentNotWithinUserRealmBusinessRuleException


class EnrolmentSecurityService:

    @classmethod
    def rule_try_can_view_enrolment(cls, user, client_enrolment):
        checks_passed = []
        c001 = EnrolmentSecurityServiceChecks.check_client_belongs_to_ip(client_enrolment, user.implementing_partner)
        if c001 is not None:
            ### DELEGATION CODE
            #c002 = EnrolmentSecurityServiceChecks.check_ip_has_active_delegation(
            #    client_enrolment.implementing_partner, user.implementing_partner)
            #if c002 is not None:
            #    checks_passed.append(c002)
        #else:
            checks_passed.append(c001)

        if checks_passed:
            return checks_passed
        else:
            raise EnrolmentNotWithinUserRealmBusinessRuleException

    @classmethod
    def rule_try_can_edit_enrolment(cls, user, client_enrolment):
        checks_passed = []
        c001 = EnrolmentSecurityServiceChecks.check_client_belongs_to_ip(client_enrolment, user.implementing_partner)
        if c001 is not None:
            checks_passed.append(c001)

        if checks_passed:
            return checks_passed
        else:
            raise EnrolmentNotWithinUserRealmBusinessRuleException

    @classmethod
    def rule_try_save_enrolment(cls, user, client_enrolment):
        checks_passed = []
        new_instance = client_enrolment.pk is None

        try:
            if not new_instance:
                rule_edit_enrolment_codes = cls.rule_try_can_edit_enrolment(user, client_enrolment)
                if not rule_edit_enrolment_codes:
                    return []
                checks_passed.extend(rule_edit_enrolment_codes)
        except Exception:
            return []

        return checks_passed
