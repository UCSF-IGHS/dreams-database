from datetime import datetime
#from DreamsApp.models import ServiceDelegation


class EnrolmentSecurityServiceChecks:

    @classmethod
    def check_client_belongs_to_ip(cls, client, implmenting_partner):
        if client.implementing_partner == implmenting_partner:
            return "C001"
        return None
    """
    @classmethod
    def check_ip_has_active_delegation(cls, main_implementing_partner, delegated_implementing_partner):
        active_delegation_records = ServiceDelegation.objects.filter(
            main_implementing_partner=main_implementing_partner,
            delegated_implementing_partner=delegated_implementing_partner,
            end_date__gte=datetime.now().date()
        )
        if active_delegation_records.count() > 0:
            return "C002"
        return None
    """