from DreamsApp.business_rules.services.intervention_security_service import InterventionSecurityService
from DreamsApp.exceptions import InterventionNotWithinUserRealmBusinessRuleException, \
    InterventionTypeNotWithinUserRealmBusinessRuleException
from DreamsApp.models import ImplementingPartnerUser
from xf.xf_services import XFModelPermissionBase


class InterventionActionPermissions(XFModelPermissionBase):

    def __init__(self, model, user, intervention=None):
        self.model = model
        self.user = user
        self.implementing_partner_user = ImplementingPartnerUser.objects.get(user=user)
        self.intervention = intervention

    def can_perform_new(self):
        perform_new = False
        try:
            checks = InterventionSecurityService.rule_try_can_add_intervention(self.implementing_partner_user,
                                                                               self.intervention)
            if checks:
                perform_new = super().can_perform_new()

        except Exception as e:
            perform_new = False

        return perform_new

    def can_perform_list(self):
        return super().can_perform_list()

    def can_perform_view(self):
        can_view = False
        try:
            checks = InterventionSecurityService.rule_try_can_view_intervention(self.implementing_partner_user,
                                                                                self.intervention)
            if checks:
                can_view = super().can_perform_details()
        except InterventionNotWithinUserRealmBusinessRuleException as e:
            can_view = False
        return can_view

    def can_perform_edit(self):
        can_edit = False
        try:
            checks = InterventionSecurityService.rule_try_can_edit_intervention(self.implementing_partner_user,
                                                                                self.intervention)
            if checks:
                can_edit = super().can_perform_edit()

        except InterventionNotWithinUserRealmBusinessRuleException as e:
            can_edit = False

        return can_edit

    def can_perform_void(self):
        return self.can_perform_edit()

    def can_perform_non_delegated_intervention_type_warning(self, client, intervention_type):

        can_warn = False
        try:
            checks = InterventionSecurityService.rule_try_can_add_intervention_type_to_client(self.user,
                                                                                         client, intervention_type)
            if checks:
                can_warn = False
        except InterventionTypeNotWithinUserRealmBusinessRuleException:
            can_warn = True
        return can_warn
