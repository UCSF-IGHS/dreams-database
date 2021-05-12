from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpRequest

from DreamsApp.business_rules.services.intervention_security_service import InterventionSecurityService
from DreamsApp.exceptions import DreamsBusinessRuleViolationException
from DreamsApp.models import Intervention
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

        # for unit tests
        if request is None:
            for frame_record in inspect.stack():
                if frame_record[3].startswith('test_'):
                    request = frame_record[0].f_locals['request'] if 'request' in frame_record[0].f_locals else None
                    if request is None:
                        return frame_record[0].f_locals['user'] if 'user' in frame_record[0].f_locals else None
                    break

        return request.user if request is not None else None

    @staticmethod
    @receiver(pre_save, sender=Intervention)
    def intervention_pre_save(sender, instance, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        user = SaveService.get_user()
        checks_passed = InterventionSecurityService.rule_try_can_add_intervention(instance,
                                                                                  user) or \
                        InterventionSecurityService.rule_try_can_edit_intervention(
            instance, user)
        if not checks_passed:
            raise DreamsBusinessRuleViolationException

