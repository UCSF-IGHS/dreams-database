import logging

from django.db import DataError
from  django.core import exceptions
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError, ParseError, UnsupportedMediaType

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from DreamsApp.api.response_status_mixin import ResponseStatusMixin
from DreamsApp.api.serializers import InterventionSerializer
from DreamsApp.cache_helpers.intervention_cache_helper import InterventionCacheHelper


class InterventionCreateView(CreateAPIView, ResponseStatusMixin):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = InterventionSerializer
    renderer_classes = [JSONRenderer]

    def create(self, request, *args, **kwargs):

        logging.info(request.data)
        serializer = self.get_serializer(data=request.data)
        response_status = None
        errors = []
        http_response_code = status.HTTP_200_OK

        try:
            self.perform_create(serializer)
            InterventionCacheHelper.refresh_cache(serializer.data['client'], serializer.data['intervention_type'])
            http_response_code = status.HTTP_201_CREATED
            response_status = ResponseStatusMixin.SUCCESS_CREATED

        except (UnsupportedMediaType, ParseError) as e:
            response_status = ResponseStatusMixin.ERROR_SERIALIZATION_ERROR
            logging.error(e)

        except ValidationError as e:
            response_status = ResponseStatusMixin.ERROR_VALIDATION_ERROR
            errors = self.extract_response_errors(e.get_codes())
            logging.error(e)

        except DataError as e:
            response_status = ResponseStatusMixin.SUCCESS_DUPLICATE_IGNORED if 'DUPLICATE' in e.args \
                else ResponseStatusMixin.ERROR_VALIDATION_ERROR
            logging.error(e)

        except exceptions.ValidationError as e:
            response_status = ResponseStatusMixin.ERROR_VALIDATION_ERROR
            logging.error(e)

        except Exception as e:
            response_status = ResponseStatusMixin.ERROR
            errors = str(e.args)
            logging.error(e)

        logging.info(response_status)
        logging.info(errors)
        return Response(status=http_response_code, data={'status': response_status, "errors": errors})

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()
