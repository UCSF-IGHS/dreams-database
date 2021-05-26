from DreamsApp.business_rules.services.intervention_security_service import InterventionSecurityService
from DreamsApp.exceptions import InterventionNotWithinUserRealmBusinessRuleException
from DreamsApp.models import ImplementingPartnerUser


class InterventionAccessActions:
    def __init__(self, user, intervention):
        self.user = user
        self.implementing_partner_user = ImplementingPartnerUser.get(user=user)
        self.intervention = intervention

    def can_perform_new(self):
        can_perform_new = False
        try:
            checks = InterventionSecurityService.rule_try_can_add_intervention(self.implementing_partner_user,
                                                                          self.intervention)
        except InterventionNotWithinUserRealmBusinessRuleException as e:
            can_perform_new =  False
        else:
            if checks:
                can_perform_new = True
        return can_perform_new

    def can_perform_view(self):
        can_perform_view = False
        try:
            checks = InterventionSecurityService.rule_try_can_view_intervention(self.implementing_partner_user,
                                                                               self.intervention)
        except InterventionNotWithinUserRealmBusinessRuleException as e:
            can_perform_view = False
        else:
            if checks:
                can_perform_view = True
        return can_perform_view

    def can_perform_edit(self):
        can_perform_edit = False
        try:
            checks = InterventionSecurityService.rule_try_can_edit_intervention(self.implementing_partner_user,
                                                                                self.intervention)
        except InterventionNotWithinUserRealmBusinessRuleException as e:
            can_perform_edit = False
        else:
            if checks:
                can_perform_edit = True
        return can_perform_edit

    def can_perform_void(self):
        can_perform_edit = False
        try:
            checks = InterventionSecurityService.rule_try_can_edit_intervention(self.implementing_partner_user,
                                                                                self.intervention)
        except InterventionNotWithinUserRealmBusinessRuleException as e:
            can_perform_edit = False
        else:
            if checks:
                can_perform_edit = True
        return can_perform_edit