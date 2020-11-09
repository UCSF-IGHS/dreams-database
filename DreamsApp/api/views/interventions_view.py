from django.db import DataError
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError, ParseError, UnsupportedMediaType
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from DreamsApp.api.serializers import InterventionSerializer
from DreamsApp.api.status_codes_mixin import StatusCodesMixin


class InterventionCreateView(CreateAPIView):
    serializer_class = InterventionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        try:
            self.perform_create(serializer)
        except (UnsupportedMediaType, ParseError) as e:
            response_body = {'status': StatusCodesMixin.ERROR_SERIALIZATION_ERROR}
            return Response(status=200, data=response_body)
        except ValidationError as e:

            response_body = {'status': StatusCodesMixin.ERROR_VALIDATION_ERROR, "errors": []}
            for field in dict(e.detail).keys():
                if field == 'hts_result':
                    response_body["errors"].append({field: StatusCodesMixin.ERROR_VALIDATION_HTS_RESULT_NOT_FOUND})
                elif field == 'pregnancy_test_result':
                    response_body["errors"].append(
                        {field: StatusCodesMixin.ERROR_VALIDATION_PREGNANCY_TEST_RESULT_NOT_FOUND})
                elif field == 'intervention_type':
                    response_body["errors"].append(
                        {field: StatusCodesMixin.ERROR_VALIDATION_INTERVENTION_TYPE_NOT_FOUND})
                elif field == 'implementing_partner':
                    response_body["errors"].append({field: StatusCodesMixin.ERROR_VALIDATION_IP_NOT_FOUND})
                elif field == 'external_organisation':
                    response_body["errors"].append(
                        {field: StatusCodesMixin.ERROR_VALIDATION_EXTERNAL_ORGANISATION_NOT_FOUND})
                elif field == 'client':
                    response_body["errors"].append({field: StatusCodesMixin.ERROR_VALIDATION_CLIENT_NOT_FOUND})
                elif field == 'created_by':
                    response_body["errors"].append({field: StatusCodesMixin.ERROR_VALIDATION_USER_NOT_FOUND})
                else:
                    response_body["errors"].append({field: StatusCodesMixin.ERROR_VALIDATION_ERROR})

            return Response(status=200, data=response_body)

        response_body = {'status': StatusCodesMixin.SUCCESS_CREATED}
        return Response(status=status.HTTP_201_CREATED, data=response_body)

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()
