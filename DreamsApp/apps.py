# coding=utf-8
from __future__ import unicode_literals

from django.apps import AppConfig


class DreamsappConfig(AppConfig):
    name = 'DreamsApp'

    def ready(self):
        from DreamsApp.business_rules.services.save_service import SaveService
