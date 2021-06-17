from datetime import datetime

from DreamsApp.constants import REFERRAL_PENDING_STATUS
from DreamsApp.models import ServiceDelegation, Referral, ReferralStatus


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
    def check_client_has_active_referral_to_ip(cls, client, ip, intervention_type):
        referral_status = ReferralStatus.objects.get(code=REFERRAL_PENDING_STATUS)
        referrals = Referral.objects.filter(client=client, intervention_type=intervention_type, receiving_ip=ip,
                                            referral_expiration_date__gte=datetime.now().date(), referral_status=referral_status)
        if referrals.exists():
            return "VI005"
        return None
