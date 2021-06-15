from django.core.exceptions import PermissionDenied
from django.db import DatabaseError

from xf.xf_services import XFBusinessRuleViolationException


class InterventionNotWithinUserRealmBusinessRuleException(XFBusinessRuleViolationException):
    pass


class EnrolmentNotWithinUserRealmBusinessRuleException(XFBusinessRuleViolationException):
    pass

class ClientSearchException(DatabaseError):
    pass

class DreamsBusinessRuleViolationException(XFBusinessRuleViolationException):
    pass

class DreamsPermissionDeniedException(PermissionDenied):
    pass

class InterventionTypeNotWithinUserRealmBusinessRuleException(XFBusinessRuleViolationException):
    pass
