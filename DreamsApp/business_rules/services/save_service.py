from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpRequest

from DreamsApp.business_rules.services.enrolment_security_service import EnrolmentSecurityService
from DreamsApp.business_rules.services.intervention_security_service import InterventionSecurityService
from DreamsApp.exceptions import DreamsBusinessRuleViolationException
from DreamsApp.models import Intervention, ImplementingPartnerUser, Client
from xf.xf_services import XFSaveService


class SaveService(XFSaveService):
    @classmethod
    def get_user(cls) -> User:

        # See https://stackoverflow.com/questions/32332329/getting-the-request-user-form-pre-save-in-django
        import inspect

        request: HttpRequest = None
        for frame_record in inspect.stack():
            if frame_record[3] == 'get_response':
                request = frame_record[0].f_locals['request']
                break

        user = None
        # for unit tests
        if request is None:
            for frame_record in inspect.stack():
                if frame_record[3].startswith('test_'):
                    request = frame_record[0].f_locals['request'] if 'request' in frame_record[0].f_locals else None
                    if request is None:
                        user = frame_record[0].f_locals['user'] if 'user' in frame_record[0].f_locals else None
                    break

        ip_user = None

        if request and request.user is not None:
            user = request.user

        if user is not None:
            ip_user = ImplementingPartnerUser.objects.get(user__id=request.user.id)

        return ip_user

    @staticmethod
    @receiver(pre_save, sender=Intervention)
    def intervention_pre_save(sender, instance, *args, **kwargs):
        user = SaveService.get_user()

        if settings.TESTING and user is None:
            pass
        else:
            checks_passed = InterventionSecurityService.rule_try_save_intervention(user, instance)
            if not checks_passed:
                raise DreamsBusinessRuleViolationException

    @staticmethod
    @receiver(pre_save, sender=Client)
    def enrolment_pre_save(sender, instance, *args, **kwargs):
        ip_user = SaveService.get_user()
        if ip_user and ip_user.user.pk:
            checks_passed = EnrolmentSecurityService.rule_try_save_enrolment(ip_user, instance)
            if not checks_passed:
                raise DreamsBusinessRuleViolationException
