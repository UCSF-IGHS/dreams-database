from datetime import datetime

from DreamsApp.models import ServiceDelegation


class InterventionSecurityServiceChecks:

    @classmethod
    def check_client_belongs_to_ip(cls, user, client):
        if user.implementing_partner == client.implementing_partner:
            return "VI002"
        return None

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

    @classmethod
    def check_intervention_type_delegated_to_user_ip_by_client_ip(cls, user, client, intervention_type):
        delegations_from_client_ip = ServiceDelegation.objects.filter(
            main_implementing_partner=client.implementing_partner,
            delegated_implementing_partner=user.implementing_partner, end_date__gte=datetime.now().date())
        if intervention_type.id in set(delegations_from_client_ip.values_list('intervention_type_id', flat=True)):
            return "VIT001"
        return None
