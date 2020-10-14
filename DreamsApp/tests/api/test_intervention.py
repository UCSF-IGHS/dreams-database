import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from DreamsApp.serializers import InterventionSerializer
from DreamsApp.models import Intervention


client = Client()
