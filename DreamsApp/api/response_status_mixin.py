class ResponseStatusMixin:

    SUCCESS_CREATED = 'SUCCESS_CREATED'
    SUCCESS_DUPLICATE_IGNORED = 'SUCCESS_DUPLICATE_IGNORED'
    SUCCESS_UPDATED = 'SUCCESS_UPDATED'
    SUCCESS_DELETED = 'SUCCESS_DELETED'
    ERROR_SERIALIZATION_ERROR = 'ERROR_SERIALIZATION_ERROR'
    ERROR_VALIDATION_ERROR = 'ERROR_VALIDATION_ERROR'
    ERROR_VALIDATION_DATE_IN_FUTURE = 'ERROR_VALIDATION_DATE_IN_FUTURE'
    ERROR_VALIDATION_CLIENT_NOT_FOUND = 'ERROR_VALIDATION_CLIENT_NOT_FOUND'
    ERROR_VALIDATION_IP_NOT_FOUND = 'ERROR_VALIDATION_IP_NOT_FOUND'
    ERROR_VALIDATION_INTERVENTION_TYPE_NOT_FOUND = 'ERROR_VALIDATION_INTERVENTION_TYPE_NOT_FOUND'
    ERROR_VALIDATION_HTS_RESULT_NOT_FOUND = 'ERROR_VALIDATION_HTS_RESULT_NOT_FOUND'
    ERROR_VALIDATION_EXTERNAL_ORGANISATION_NOT_FOUND = 'ERROR_VALIDATION_EXTERNAL_ORGANISATION_NOT_FOUND'
    ERROR_VALIDATION_PREGNANCY_TEST_RESULT_NOT_FOUND = 'ERROR_VALIDATION_PREGNANCY_TEST_RESULT_NOT_FOUND'
    ERROR_VALIDATION_USER_NOT_FOUND = 'ERROR_VALIDATION_USER_NOT_FOUND'
    ERROR_VALIDATION_ODK_UUID_MISSING = 'ERROR_VALIDATION_ODK_UUID_NOT_FOUND'
    ERROR_ACCESS_DENIED = 'ERROR_ACCESS_DENIED'

    def extract_response_errors(self, error_codes):
        response_errors = []
        for field in error_codes.keys():
            if field == 'hts_result':
                response_errors.append({field: ResponseStatusMixin.ERROR_VALIDATION_HTS_RESULT_NOT_FOUND})
            elif field == 'pregnancy_test_result':
                response_errors.append(
                    {field: ResponseStatusMixin.ERROR_VALIDATION_PREGNANCY_TEST_RESULT_NOT_FOUND})
            elif field == 'intervention_type':
                response_errors.append(
                    {field: ResponseStatusMixin.ERROR_VALIDATION_INTERVENTION_TYPE_NOT_FOUND})
            elif field == 'implementing_partner':
                response_errors.append({field: ResponseStatusMixin.ERROR_VALIDATION_IP_NOT_FOUND})
            elif field == 'external_organisation':
                response_errors.append(
                    {field: ResponseStatusMixin.ERROR_VALIDATION_EXTERNAL_ORGANISATION_NOT_FOUND})
            elif field == 'client':
                response_errors.append({field: ResponseStatusMixin.ERROR_VALIDATION_CLIENT_NOT_FOUND})
            elif field == 'created_by':
                response_errors.append({field: ResponseStatusMixin.ERROR_VALIDATION_USER_NOT_FOUND})
            elif field == 'odk_uuid':
                response_errors.append({field: ResponseStatusMixin.ERROR_VALIDATION_ODK_UUID_MISSING})
            else:
                response_errors.append({field: ResponseStatusMixin.ERROR_VALIDATION_ERROR})

        return response_errors