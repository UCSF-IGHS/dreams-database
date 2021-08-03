from DreamsApp.business_rules.check_rules.intervention_security_service_checks import InterventionSecurityServiceChecks
from DreamsApp.exceptions import InterventionNotWithinUserRealmBusinessRuleException


class InterventionSecurityService:

    @classmethod
    def rule_try_can_view_intervention(cls, user, intervention):
        checks_passed = []
        vI002 = InterventionSecurityServiceChecks.check_client_belongs_to_ip(user, intervention.client)

        if vI002 is None:
            vI003 = InterventionSecurityServiceChecks.check_intervention_belongs_to_ip(
                user, intervention)
            if vI003 is None:
                vI004 = InterventionSecurityServiceChecks.check_ip_has_active_delegation(
                    intervention.client.implementing_partner, user.implementing_partner)
                if vI004 is not None:
                    checks_passed.append(vI004)
            else:
                checks_passed.append(vI003)
        else:
            checks_passed.append(vI002)
        if checks_passed:
            return checks_passed
        else:
            raise InterventionNotWithinUserRealmBusinessRuleException

    @classmethod
    def rule_try_can_add_intervention(cls, user, intervention):
        checks_passed = []
        vI002 = InterventionSecurityServiceChecks.check_client_belongs_to_ip(user, intervention.client)
        if vI002 is None:
            # vI004 = InterventionSecurityServiceChecks.check_ip_has_active_delegation(
            #     intervention.client.implementing_partner, user.implementing_partner)
            # if vI004 is not None:
            #     checks_passed.append(vI004)
            # else:
            vI005 = InterventionSecurityServiceChecks.check_client_has_active_referral_to_ip(
                intervention.client, user.implementing_partner, intervention.intervention_type)
            if vI005 is not None:
                checks_passed.append(vI005)
        else:
            checks_passed.append(vI002)
        if checks_passed:
            return checks_passed
        else:
            raise InterventionNotWithinUserRealmBusinessRuleException

    @classmethod
    def rule_try_can_edit_intervention(cls, user, intervention):
        checks_passed = []
        vI003 = InterventionSecurityServiceChecks.check_intervention_belongs_to_ip(
            user, intervention)
        if vI003 is None:
            raise InterventionNotWithinUserRealmBusinessRuleException
        else:
            checks_passed.append(vI003)
        return checks_passed

    @classmethod
    def rule_try_can_delete_intervention(cls, user, intervention):
        checks_passed = cls.rule_try_can_edit_intervention(user, intervention)
        return checks_passed

    @classmethod
    def rule_try_save_intervention(cls, user, intervention) -> []:
        checks_passed = []
        new_instance = intervention.pk is None

        try:
            if new_instance:
                rule_add_intervention_codes = cls.rule_try_can_add_intervention(user, intervention)
                if not rule_add_intervention_codes:
                    return []
                checks_passed.extend(rule_add_intervention_codes)
            else:
                rule_edit_intervention_codes = cls.rule_try_can_edit_intervention(user, intervention)
                if not rule_edit_intervention_codes:
                    return []
                checks_passed.extend(rule_edit_intervention_codes)
        except Exception:
            return []

        return checks_passed
