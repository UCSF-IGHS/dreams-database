from django.db import DataError
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError, ParseError, UnsupportedMediaType
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from DreamsApp.api.serializers import InterventionSerializer
from DreamsApp.api.response_status_mixin import ResponseStatusMixin


class InterventionCreateView(CreateAPIView, ResponseStatusMixin):
    serializer_class = InterventionSerializer
    renderer_classes = [JSONRenderer]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        try:
            self.perform_create(serializer)
        except (UnsupportedMediaType, ParseError) as e:
            response_body = {'status': self.ERROR_SERIALIZATION_ERROR}
            return Response(status=200, data=response_body)

        except ValidationError as e:
            errors = self.extract_response_errors(e.get_codes())
            response_body = {'status': self.ERROR_VALIDATION_ERROR, "errors": errors}
            return Response(status=200, data=response_body)

        except DataError as e:
            response_body = {'status': self.SUCCESS_DUPLICATE_IGNORED, 'message': 'Success'}
            return Response(status=status.HTTP_200_OK, data=response_body)

        response_body = {'status': self.SUCCESS_CREATED}
        return Response(status=status.HTTP_201_CREATED, data=response_body)

    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()
