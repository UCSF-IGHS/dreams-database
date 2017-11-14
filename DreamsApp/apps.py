# coding=utf-8
from __future__ import unicode_literals

from django.apps import AppConfig


class DreamsappConfig(AppConfig):
    name = 'DreamsApp'

    def ready(self):
        print("at ready")
        import DreamsApp.signals
