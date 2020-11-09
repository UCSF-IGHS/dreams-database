from DreamsApp.api.status_codes_mixin import StatusCodesMixin
from DreamsApp.models import Intervention
from DreamsApp.tests.api.api_test_case import APITestCase


class InterventionAPITestCase(APITestCase):

    def test_request_with_no_authentication_returns_unauthorised(self):
        test_data = self._generate_test_data()
        response = self._send_request(None, test_data['request_body'])
        self.assertEquals(response.status_code, 403, "Expected response status code of 403 for unauthorized")

    def test_with_wrong_username_returns_a_user_field_validation_error(self):
        test_data = self._generate_test_data()
        test_data['request_body']['created_by'] = 'unknown_user'

        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, 200, "Expected response status code of 200")
        self.assertEquals(response.data["status"], StatusCodesMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

        created_by_field_error = {'created_by': StatusCodesMixin.ERROR_VALIDATION_USER_NOT_FOUND}
        self.assertIn(created_by_field_error, response.data["errors"],
                      'Expected created_by field amongst the returned error fields')

    def test_request_body_with_null_client_id_returns_a_client_field_validation_error(self):
        test_data = self._generate_test_data()
        test_data['request_body']['client'] = None

        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, 200, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.data["status"], StatusCodesMixin.ERROR_VALIDATION_ERROR,
                          'Expected ERROR_VALIDATION_ERROR status code.')

        client_field_error = {'created_by': StatusCodesMixin.ERROR_VALIDATION_CLIENT_NOT_FOUND}
        self.assertIn(client_field_error, response.data["errors"],
                      'Expected client field amongst the returned error fields')

    def test_request_with_wrong_hts_result_returns_hts_result_field_validation_error(self):
        wrong_hts_result = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['hts_result'] = wrong_hts_result

        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, 200, "Expected response status code of 200")
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.body.status, StatusCodesMixin.ERROR_SERIALIZATION_ERROR,
                          'Expected ERROR_SERIALIZATION_ERROR status code.')

    def test_request_with_wrong_pregnancy_test_result_returns_bad_request(self):
        wrong_pregnancy_test_result = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['pregnancy_test_result'] = wrong_pregnancy_test_result

        response = self._send_request(test_data['user'], test_data['request_body'])

        self.assertEquals(response.status_code, 200,
                          "Expected response status code of 200 but instead received {}".format(response.status_code))
        self.assertEquals(response.status_text, 'Bad Request',
                          "Expected response status code of Bad Request but instead received {}".format(
                              response.status_text))
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.body.status, StatusCodesMixin.ERROR_SERIALIZATION_ERROR,
                          'Expected ERROR_SERIALIZATION_ERROR status code.')

    def test_request_with_wrong_intervention_type_returns_bad_request(self):
        WRONG_INTERVENTION_TYPE = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['intervention_type'] = WRONG_INTERVENTION_TYPE
        response = self._send_request(test_data['user'], test_data['request_body'])
        self.assertEquals(response.status_code, 200,
                          "Expected response status code of 200 but instead received {}".format(response.status_code))
        self.assertEquals(response.status_text, 'Bad Request',
                          "Expected response status code of Bad Request but instead received {}".format(
                              response.status_text))
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.body.status, StatusCodesMixin.ERROR_SERIALIZATION_ERROR,
                          'Expected ERROR_SERIALIZATION_ERROR status code.')

    def test_request_with_wrong_implementing_partner_returns_bad_request(self):
        WRONG_IMPLEMENTING_PARTNER = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['external_organisation'] = WRONG_IMPLEMENTING_PARTNER
        response = self._send_request(test_data['user'], test_data['request_body'])
        self.assertEquals(response.status_code, 200,
                          "Expected response status code of 200 but instead received {}".format(response.status_code))
        self.assertEquals(response.status_text, 'Bad Request',
                          "Expected response status code of Bad Request but instead received {}".format(
                              response.status_text))
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.body.status, StatusCodesMixin.ERROR_SERIALIZATION_ERROR,
                          'Expected ERROR_SERIALIZATION_ERROR status code.')

    def test_request_with_wrong_external_organisation_returns_bad_request(self):
        WRONG_EXTERNAL_ORGANISATION = 9999
        test_data = self._generate_test_data()
        test_data['request_body']['external_organisation'] = WRONG_EXTERNAL_ORGANISATION
        response = self._send_request(test_data['user'], test_data['request_body'])
        self.assertEquals(response.status_code, 200,
                          "Expected response status code of 200 but instead received {}".format(response.status_code))
        self.assertEquals(response.status_text, 'Bad Request',
                          "Expected response status code of Bad Request but instead received {}".format(
                              response.status_text))
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.body.status, StatusCodesMixin.ERROR_SERIALIZATION_ERROR,
                          'Expected ERROR_SERIALIZATION_ERROR status code.')

    def test_empty_request_body_returns_bad_request(self):
        test_data = self._generate_test_data()
        response = self._send_request(test_data['user'], {})
        self.assertEquals(response.status_code, 200,
                          "Expected response status code of 200 but instead received {}".format(response.status_code))
        self.assertEquals(response.status_text, 'Bad Request',
                          "Expected response status code of Bad Request but instead received {}".format(
                              response.status_text))
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database after the api request")
        self.assertEquals(response.body.status, StatusCodesMixin.ERROR_SERIALIZATION_ERROR,
                          'Expected ERROR_SERIALIZATION_ERROR status code.')

    def test_intervention_request_creates_a_record(self):
        test_data = self._generate_test_data()
        self.assertEquals(Intervention.objects.all().count(), 0,
                          "Expected no record from the database before the api request")
        response = self._send_request(test_data['user'], test_data['request_body'])
        self.assertEquals(response.status_code, 201,
                          "Expected response status code of 201")
        self.assertEquals(response.data["status"], StatusCodesMixin.SUCCESS_CREATED,
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
        self._send_request(test_data['user'], test_data['request_body'])
        self.assertEquals(Intervention.objects.all().count(), 1,
                          "Expected one record from the database after second api call")

        self.assertEquals(response.data["status"], StatusCodesMixin.SUCCESS_CREATED,
                          'Expected SUCCESS_CREATED status code.')
