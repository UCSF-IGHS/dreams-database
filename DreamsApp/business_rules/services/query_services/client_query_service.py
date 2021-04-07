from DreamsApp.business_rules.check_rules.enrolment_security_service_checks import EnrolmentSecurityServiceChecks
from DreamsApp.exceptions import EnrolmentNotWithinUserRealmBusinessRuleException


class ClientQueryService:

    def __init__(self, ip_user):
        self.ip_user = ip_user

    def get_clients(self, search_string=None, implementing_partner=None):
        pass
