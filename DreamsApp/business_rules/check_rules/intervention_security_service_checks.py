from datetime import datetime

from DreamsApp.exceptions import DreamsPermissionDeniedException
from DreamsApp.models import ServiceDelegation


class InterventionSecurityServiceChecks:

    @classmethod
    def check_client_belongs_to_ip(cls, user, client):
        if user is not None:
            if user.implementing_partner is not client.implementing_partner:
                raise DreamsPermissionDeniedException(
                    'User implementing partner not equal to client implementing partner')
        return "VI002"

    @classmethod
    def check_ip_has_active_delegation(cls, main_implementing_partner, delegated_implementing_partner):
        active_delegation_records = ServiceDelegation.objects.filter(
            main_implementing_partner=main_implementing_partner,
            delegated_implementing_partner=delegated_implementing_partner,
            end_date__gte=datetime.now().date()
        )
        if active_delegation_records.count() > 0:
            return "VI004"
        return None

    @classmethod
    def check_intervention_belongs_to_ip(cls, user, intervention):
        if user.implementing_partner == intervention.implementing_partner:
            return "VI003"
        return None
