import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from DreamsApp.serializers import InterventionSerializer
from DreamsApp.models import Intervention


class GetAllInterventionsTest(TestCase):
    """ Test module for GET all interventions API """

    def setUp(self):
        client = Client()

        # Intervention.objects.create(
        #     name='Casper', age=3, breed='Bull Dog', color='Black')

    def test_get_all_intervention(self):
        # get API response
        response = client.get(reverse('get_post_puppies'))
        # get data from db
        interventions = Intervention.objects.all()
        serializer = InterventionSerializer(interventions, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
