from django.db import DataError
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from DreamsApp.api.serializers import InterventionSerializer
from DreamsApp.api.status_codes_mixin import StatusCodesMixin


class InterventionCreateView(CreateAPIView):
    serializer_class = InterventionSerializer
    renderer_classes = [JSONRenderer]

    def perform_create(self, serializer):
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]

        try:
            interventions = self.request.data
            if not self.request.data:
                return Response(
                    status=200, data={"message": "The request body was empty"}
                )

            serializer = InterventionSerializer(data=interventions)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = {'message': StatusCodesMixin.SUCCESS_CREATED},
                return Response(
                    status=status.HTTP_201_CREATED,
                    data=data,
                )
            return Response(status=200)
        except DataError as e:
            return Response(status=200, data={"message": str(e)})
        except Exception as e:
            return Response(status=200, data={"message": str(e)})
