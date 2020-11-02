from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from datetime import date, timedelta
from DreamsApp.api.views.interventions import InterventionMultipleCreateView
from DreamsApp.tests.factories.factories import (
    ExternalOrganisationFactory,
    ExternalOrganisationTypeFactory,
    InterventionTypeFactory,
    InterventionCategoryFactory,
    HTSResultFactory,
    PregnancyTestResultFactory,
    ImplementingPartnerFactory,
)
from DreamsApp.models import Client, ExternalOrganisation, Intervention


class InterventionAPITestCase(TestCase):
    def setUp(self):
        self.interventions = [
            {
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
                "created_by": "api_user",
                "implementing_partner": 6,
                "external_organisation": None,
                "external_organization_other": None,
            },
        ]

    def tearDown(self):
        del self.interventions

    def test_with_no_authentication_is_unauthorised(self):
        factory = APIRequestFactory()
        request = factory.post("api/v1/interventions")
        view = InterventionMultipleCreateView.as_view()
        response = view(request)
        assert response.status_code == 401
        assert response.status_text == "Unauthorized"

    def test_authenticated_request_with_empty_body_responds_with_bad_request(self):
        user = User.objects.create(username="adventure", password="No1Knows!t")
        factory = APIRequestFactory()
        request = factory.post("api/v1/interventions")
        force_authenticate(request, user)
        view = InterventionMultipleCreateView.as_view()
        response = view(request)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data["message"] == "The request body was empty"

    def test_authenticated_request_with_empty_array_body_responds_with_bad_request(
            self,
    ):
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self.interventions = []
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data["message"] == "The request body was empty"

    def test_authenticated_request_with_wrong_client_returns_400(self):
        WRONG_CLIENT_ID = 99999
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["client"] = WRONG_CLIENT_ID
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data[
                   "message"
               ] == [{'client': ['Object with id={} does not exist.'.format(WRONG_CLIENT_ID)]}]

    def test_authenticated_request_with_wrong_intervention_type_returns_400(self):
        WRONG_INTERVENTION_TYPE = 99999
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["intervention_type"] = WRONG_INTERVENTION_TYPE
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data[
                   "message"
               ] == [{'intervention_type': ['Object with code={} does not exist.'.format(WRONG_INTERVENTION_TYPE)]}]

    def test_authenticated_request_with_wrong_external_organization_returns_400(self):
        WRONG_EXTERNAL_ORGANISATION = 9999
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["external_organisation"] = WRONG_EXTERNAL_ORGANISATION
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data[
                   "message"
               ] == [{'external_organisation': [
            'Object with code={} does not exist.'.format(WRONG_EXTERNAL_ORGANISATION)]}]

    def test_authenticated_request_with_wrong_hts_result_returns_400(self):
        WRONG_HTS_RESULT = 9999
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["hts_result"] = WRONG_HTS_RESULT
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data[
                   "message"
               ] == [{'hts_result': ['Object with code={} does not exist.'.format(WRONG_HTS_RESULT)]}]

    def test_authenticated_request_with_wrong_pregnancy_test_returns_400(self):
        MISSING_PREGNANCY_TEST = 9999
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["pregnancy_test_result"] = MISSING_PREGNANCY_TEST
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data[
                   "message"
               ] == [{'pregnancy_test_result': ['Object with code={} does not exist.'.format(MISSING_PREGNANCY_TEST)]}]

    def test_authenticated_request_with_wrong_implementing_partner_test_returns_404(
            self,
    ):
        IMPLENTING_PARTNER_NOT_IN_DATABASE = 9999
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0][
            "implementing_partner"
        ] = IMPLENTING_PARTNER_NOT_IN_DATABASE
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data[
                   "message"
               ] == [{'implementing_partner': [
            'Object with code={} does not exist.'.format(IMPLENTING_PARTNER_NOT_IN_DATABASE)]}]

    def test_authenticated_request_with_wrong_user_returns_400(self):
        WRONG_USERNAME = "user_who_did_not_create_the_intervention"
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["created_by"] = "user_who_did_not_create_the_intervention"
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data["message"] == [
            {'created_by': ['Object with username={} does not exist.'.format(WRONG_USERNAME)]}]

    def test_authenticated_request_with_valid_request_data_creates_record(self):
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["hts_result"] = None
        response = self._send_request(user)
        assert response.status_code == 201
        assert response.status_text == "Created"
        assert response.data["message"] == "Success! Records successfully created"

    def test_authenticated_request_with_no_client_id_supplied_returns_400(self):
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        del self.interventions[0]["client"]
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data["message"] == [{"client": ["This field is required."]}]

    def test_authenticated_request_with_wrong_client_id_supplied_returns_400(self):
        WRONG_CLIENT_ID = 99999
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["client"] = WRONG_CLIENT_ID
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data["message"] == [{"client": ["Object with id={} does not exist.".format(WRONG_CLIENT_ID)]}]

    def test_authenticated_request_with_null_client_id_supplied_returns_400(self):
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["client"] = None
        response = self._send_request(user)
        assert response.status_code == 400
        assert response.status_text == "Bad Request"
        assert response.data["message"] == [{"client": ["This field may not be null."]}]

    def test_authenticated_user_with_duplicate_intervention_submission_returns_200(self):
        user = User.objects.create(username="adventure", password="No1Knows!t")
        self._setup_intervention(user)
        self.interventions[0]["hts_result"] = None
        response = self._send_request(user)
        assert response.status_code == 201
        assert response.status_text == "Created"
        assert response.data["message"] == "Success! Records successfully created"
        new_response = self._send_request(user)
        assert new_response.status_code == 200
        assert new_response.status_text == "OK"
        assert new_response.data["message"] == "Duplicate Record! Record not created since its a duplicate."

    def _setup_intervention(self, user):
        client = Client.objects.create(
            first_name="Lady",
            last_name="Bird",
            date_of_enrollment=date.today() - timedelta(5),
        )
        intervention_category = InterventionCategoryFactory()
        intervention_type = InterventionTypeFactory(
            intervention_category_id=intervention_category.id
        )
        external_organisation_type = ExternalOrganisationTypeFactory()
        external_organisation = ExternalOrganisationFactory(
            type_id=external_organisation_type.id
        )
        pregnancy_test_result = PregnancyTestResultFactory()
        implementing_partner = ImplementingPartnerFactory()
        self.interventions[0]["client"] = client.id
        self.interventions[0]["intervention_type"] = intervention_type.code
        self.interventions[0]["hts_result"] = None
        self.interventions[0]["external_organisation"] = external_organisation.code
        self.interventions[0]["pregnancy_test_result"] = pregnancy_test_result.code
        self.interventions[0]["created_by"] = user.username
        self.interventions[0]["implementing_partner"] = implementing_partner.code

    def _send_request(self, user):
        factory = APIRequestFactory()
        request = factory.post(
            "api/v1/interventions", self.interventions, format="json"
        )
        force_authenticate(request, user)
        view = InterventionMultipleCreateView.as_view()
        response = view(request)
        return response
