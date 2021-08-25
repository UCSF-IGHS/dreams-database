from DreamsApp.business_rules.services.enrolment_security_service import EnrolmentSecurityService
from DreamsApp.models import ImplementingPartnerUser, Client
from xf.xf_services import XFModelPermissionBase


class ClientActionPermissions(XFModelPermissionBase):

    def __init__(self, model, user, enrolment=None, *args, **kwargs):
        self.model = model
        self.user = user
        self.implementing_partner_user = ImplementingPartnerUser.objects.get(user=user)
        self.enrolment = enrolment

    def can_perform_new(self):
        if self.implementing_partner_user:
            return super().can_perform_new()
        return False

    def can_perform_list(self):
        if self.implementing_partner_user:
            return super().can_perform_list()
        return False

    def can_perform_view(self):
        can_view = False
        try:
            checks = EnrolmentSecurityService.rule_try_can_view_enrolment(self.implementing_partner_user,
                                                                          self.enrolment)
            if checks:
                can_view = super().can_perform_details()

        except Exception:
            can_view = False

        return can_view

    def can_perform_edit(self):
        can_edit = False
        try:
            checks = EnrolmentSecurityService.rule_try_can_edit_enrolment(self.implementing_partner_user,
                                                                          self.enrolment)
            if checks:
                can_edit = super().can_perform_edit()

        except Exception:
            can_edit = False

        return can_edit

    def can_perform_void(self):
        return self.can_perform_edit()
