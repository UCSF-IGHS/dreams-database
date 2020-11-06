from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from DreamsApp.api.views.interventions_view import InterventionCreateView
from DreamsApp.models import Client


class APITestCase(TestCase):
    fixtures = ['test_verification_document','test_marital_status','test_user', 'test_intervention_category', 'test_intervention_type', 'test_county',
                'implementing_partner_funder',  'test_implementing_partner', 'external_organisation_type',
                'external_organisation', 'test_sub_county', 'test_ward', 'test_client', 'test_hts_result',
                'test_pregnancy_test_result']

    def _send_request(self, user = None, interventions = {}):
        factory = APIRequestFactory()
        request = factory.post(
            "api/v1/interventions", interventions, format="json"
        )
        if user is not None:
            force_authenticate(request, user)
        view = InterventionCreateView.as_view()
        response = view(request)
        return response


    def _generate_test_data(self):
        test_data = {}
        test_data['user'] = User.objects.create(username="adventure", password="No1Knows!t")
        test_data['client'] = Client.objects.first()
        test_data['request_body'] = {
                "intervention_date": date.today(),
                "client": 1,
                "dreams_id": "2/2/2222",
                "intervention_type": 1002,
                "name_specified": None,
                "hts_result": 201,
                "pregnancy_test_result": 101,
                "client_ccc_number": None,
                "date_linked_to_ccc": None,
                "number_of_sessions_attended": None,
                "comment": None,
                "created_by": "admin",
                "implementing_partner": 3,
                "external_organisation": None,
                "external_organization_other": None,
            }
        return test_data





