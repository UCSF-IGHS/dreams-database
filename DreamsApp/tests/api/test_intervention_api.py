from rest_framework import status

from DreamsApp.api.response_status_mixin import ResponseStatusMixin
from DreamsApp.models import Intervention
from DreamsApp.tests.api.api_test_case import APITestCase


class InterventionAPITestCase(APITestCase):

    def test_request_with_no_authentication_returns_unauthorised(self):
        response = self._send_request_without_data()
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED,
                          "Expected response status code of 401 for forbidden")

    def test_with_wrong_username_returns_a_user_field_validation_error(self):
        test_data = self._generate_test_data()
        test_data['request_body']['created_by'] = 'unknown_user'

        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, status.HTTP_200_OK, "Expected response status code of 200")
        self.assertEquals(response.data["status"], ResponseStatusMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

        created_by_field_error = {'created_by': ResponseStatusMixin.ERROR_VALIDATION_USER_NOT_FOUND}
        self.assertIn(created_by_field_error, response.data["errors"],
                      'Expected created_by field amongst the returned error fields')

    def test_request_body_with_null_client_id_returns_a_client_field_validation_error(self):
        test_data = self._generate_test_data()
        test_data['request_body']['client'] = None

        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, status.HTTP_200_OK, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.data["status"], ResponseStatusMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

        client_field_error = {'client': ResponseStatusMixin.ERROR_VALIDATION_CLIENT_NOT_FOUND}
        self.assertIn(client_field_error, response.data["errors"],
                      'Expected client field amongst the returned error fields')

    def test_request_with_wrong_hts_result_returns_hts_result_field_validation_error(self):
        wrong_hts_result = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['hts_result'] = wrong_hts_result

        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, status.HTTP_200_OK, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.data['status'], ResponseStatusMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

        hts_result_field_error = {'hts_result': ResponseStatusMixin.ERROR_VALIDATION_HTS_RESULT_NOT_FOUND}
        self.assertIn(hts_result_field_error, response.data["errors"],
                      'Expected client field amongst the returned error fields')

    def test_request_with_wrong_pregnancy_test_result_returns_pregnancy_test_result_field_validation_error(self):
        wrong_pregnancy_test_result = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['pregnancy_test_result'] = wrong_pregnancy_test_result

        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, status.HTTP_200_OK, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.data['status'], ResponseStatusMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

        pregnancy_test_result_field_error = {
            'pregnancy_test_result': ResponseStatusMixin.ERROR_VALIDATION_PREGNANCY_TEST_RESULT_NOT_FOUND}
        self.assertIn(pregnancy_test_result_field_error, response.data["errors"],
                      'Expected client field amongst the returned error fields')

    def test_request_with_wrong_intervention_type_returns_intervention_type_field_validation_error(self):
        wrong_intervention_type = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['intervention_type'] = wrong_intervention_type
        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, status.HTTP_200_OK, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.data['status'], ResponseStatusMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

        intervention_type_field_error = {
            'intervention_type': ResponseStatusMixin.ERROR_VALIDATION_INTERVENTION_TYPE_NOT_FOUND}
        self.assertIn(intervention_type_field_error, response.data["errors"],
                      'Expected client field amongst the returned error fields')

    def test_request_with_wrong_implementing_partner_returns_implementing_partner_field_validation_error(self):
        wrong_implementing_partner = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['implementing_partner'] = wrong_implementing_partner
        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, status.HTTP_200_OK, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.data['status'], ResponseStatusMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

        implementing_partner_field_error = {
            'implementing_partner': ResponseStatusMixin.ERROR_VALIDATION_IP_NOT_FOUND}
        self.assertIn(implementing_partner_field_error, response.data["errors"],
                      'Expected client field amongst the returned error fields')

    def test_request_with_wrong_external_organisation_returns_external_organisation_field_validation_error(self):
        wrong_external_organisation = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['external_organisation'] = wrong_external_organisation
        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, status.HTTP_200_OK, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.data['status'], ResponseStatusMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

        external_organisation_field_error = {
            'external_organisation': ResponseStatusMixin.ERROR_VALIDATION_EXTERNAL_ORGANISATION_NOT_FOUND}
        self.assertIn(external_organisation_field_error, response.data["errors"],
                      'Expected client field amongst the returned error fields')

    def test_empty_request_body_returns_validation_error(self):
        test_data = self._generate_test_data()
        response = self._send_request(test_data['user'], {})
        self.assertEquals(response.status_code, status.HTTP_200_OK, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.data['status'], ResponseStatusMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

    def test_intervention_request_creates_a_record(self):
        test_data = self._generate_test_data()
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database before the api request")
        response = self._send_request(test_data['user'], test_data['request_body'])
        self.assertEquals(response.status_code, status.HTTP_201_CREATED, "Expected response status code of 201")
        self.assertEquals(response.data["status"], ResponseStatusMixin.SUCCESS_CREATED,
                          'Expected SUCCESS_CREATED status code.')
        self.assertEquals(Intervention.objects.all().count(), 1,
                          "Expected one record from the database after the api request")

    def test_intervention_does_not_create_duplicate_records(self):
        test_data = self._generate_test_data()
        self.assertEquals(Intervention.objects.all().count(), 0,
                          'Expected 0 interventions in the database before calling the api')
        self._send_request(test_data['user'], test_data['request_body'])
        self.assertEquals(Intervention.objects.all().count(), 1,
                          "Expected one record from the database after the first api request")

        response = self._send_request(test_data['user'], test_data['request_body'])
        self.assertEquals(response.status_code, status.HTTP_200_OK, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 1,
                          "Expected one record from the database after second api call")

        self.assertEquals(response.data["status"], ResponseStatusMixin.SUCCESS_DUPLICATE_IGNORED,
                          'Expected SUCCESS_CREATED status code.')
