from DreamsApp.business_rules.services.enrolment_security_service import EnrolmentSecurityService
from DreamsApp.exceptions import EnrolmentNotWithinUserRealmBusinessRuleException
from DreamsApp.models import ImplementingPartnerUser


class ClientAccessActions:
    def __init__(self, user, enrolment):
        self.user = user
        self.implementing_partner_user = ImplementingPartnerUser.get(user=user)
        self.enrolment = enrolment

    def can_perform_new(self):
        if self.implementing_partner_user:
            return True
        return False

    def can_perform_view(self):
        can_view = False
        try:
            checks = EnrolmentSecurityService.rule_try_can_view_enrolment(self.implementing_partner_user,
                                                                          self.enrolment)
        except EnrolmentNotWithinUserRealmBusinessRuleException as e:
            can_view = False
        else:
            if checks:
                can_view = True
        return can_view

    def can_perform_edit(self):
        can_edit = False
        try:
            checks = EnrolmentSecurityService.rule_try_can_edit_enrolment(self.implementing_partner_user,
                                                                          self.enrolment)
        except EnrolmentNotWithinUserRealmBusinessRuleException as e:
            can_edit = False
        else:
            if checks:
                can_edit = True
        return can_edit

    def can_perform_void(self):
        can_void = True
        try:
            checks = EnrolmentSecurityService.rule_try_can_edit_enrolment(self.implementing_partner_user,
                                                                          self.enrolment)
        except EnrolmentNotWithinUserRealmBusinessRuleException as e:
            can_void = False
        else:
            if checks:
                can_void = True
        return can_void
