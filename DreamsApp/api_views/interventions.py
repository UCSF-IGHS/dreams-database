from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from DreamsApp.models import Intervention
from DreamsApp.serializers import InterventionSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_interventions(request, pk):
    try:
        intervention = Intervention.objects.get(pk=pk)
    except Intervention.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single intervention
    if request.method == 'GET':
        return Response({})


@api_view(['GET', 'POST'])
def get_post_interventions(request):
    # get all interventions
    if request.method == 'GET':
        return Response({})
    # insert a new rec  ord for a puppy
    elif request.method == 'POST':
        return Response({})
