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
                if vI004 is None:
                    raise InterventionNotWithinUserRealmBusinessRuleException
                else:
                    checks_passed.append(vI004)
            else:
                checks_passed.append(vI003)
        else:
            checks_passed.append("VI002")
        return checks_passed

    @classmethod
    def rule_try_can_add_intervention(self, user, intervention):
        checks_passed = []
        vI002 = InterventionSecurityServiceChecks.check_client_belongs_to_ip(user, intervention.client)
        if vI002 is None:
            vI004 = InterventionSecurityServiceChecks.check_ip_has_active_delegation(
                intervention.client.implementing_partner, user.implementing_partner)
            if vI004 is None:
                raise InterventionNotWithinUserRealmBusinessRuleException
            else:
                checks_passed.append(vI004)
        else:
            checks_passed.append(vI002)
        return checks_passed

    @classmethod
    def rule_try_can_edit_intervention(self, user, intervention):
        checks_passed = []
        vI003 = InterventionSecurityServiceChecks.check_intervention_belongs_to_ip(
            user, intervention)
        if vI003 is None:
            raise InterventionNotWithinUserRealmBusinessRuleException
        else:
            checks_passed.append(vI003)
        return checks_passed