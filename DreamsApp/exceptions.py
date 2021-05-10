from django.db import DatabaseError

from xf.xf_services import XFBusinessRuleViolationException


class InterventionNotWithinUserRealmBusinessRuleException(XFBusinessRuleViolationException):
    pass


class EnrolmentNotWithinUserRealmBusinessRuleException(XFBusinessRuleViolationException):
    pass

class ClientSearchException(DatabaseError):
    pass
