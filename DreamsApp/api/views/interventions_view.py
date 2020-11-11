from django.db import DataError
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError, ParseError, UnsupportedMediaType
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from DreamsApp.api.response_status_mixin import ResponseStatusMixin
from DreamsApp.api.serializers import InterventionSerializer
from DreamsApp.cache_helpers.intervention_cache_helper import InterventionCacheHelper


class InterventionCreateView(CreateAPIView, ResponseStatusMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = InterventionSerializer
    renderer_classes = [JSONRenderer]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        response_status = None
        errors = []
        http_response_code = status.HTTP_200_OK

        try:
            self.perform_create(serializer)
            InterventionCacheHelper.delete_intervention_category_key_from_cache(serializer.data['client'],
                                                                                serializer.data['intervention_type'])
            http_response_code = status.HTTP_201_CREATED
            response_status = ResponseStatusMixin.SUCCESS_CREATED

        except (UnsupportedMediaType, ParseError) as e:
            response_status = ResponseStatusMixin.ERROR_SERIALIZATION_ERROR

        except ValidationError as e:
            response_status = ResponseStatusMixin.ERROR_VALIDATION_ERROR
            errors = self.extract_response_errors(e.get_codes())

        except DataError as e:
            response_status = ResponseStatusMixin.SUCCESS_DUPLICATE_IGNORED

        return Response(status=http_response_code, data={'status': response_status, "errors": errors})

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()
