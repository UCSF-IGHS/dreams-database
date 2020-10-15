from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.contrib.auth.models import User
from DreamsApp.models import Intervention, Client, InterventionType, HTSResult, ExternalOrganisation, ImplementingPartner, PregnancyTestResult
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
        intervention_date = datetime.strptime(
            request.data.get('intervention_date'),  '%Y-%m-%d')

        client = Client.objects.get(pk=int(request.data.get('client_id')))
        intervention_type = InterventionType.objects.get(
            code=int(request.data.get('intervention_type')))

        hts_result = request.data.get('hts_result')
        if hts_result:
            hts_result = HTSResult.objects.get(
                code=int(hts_result))

        external_organisation = request.data.get('external_organisation')
        if external_organisation:
            external_organization = ExternalOrganisation.objects.get(
                code=int(external_organization))

        pregnancy_test_result = request.data.get('pregnancy_test_result')

        if pregnancy_test_result:
            pregnancy_test_result = PregnancyTestResult.objects.get(
                code=int(pregnancy_test_result))

        implementing_partner = request.data.get('implementing_partner')
        if implementing_partner:
            implementing_partner = ImplementingPartner.objects.get(
                code=int(implementing_partner))

        created_by = request.data.get('created_by')
        if created_by:
            created_by = User.objects.get(username=created_by)

        external_organization = request.data.get('external_organization')
        if external_organization:
            external_organization = ExternalOrganisation.objects.get(
                code=external_organization)

        date_linked_to_ccc = request.data.get('date_linked_to_ccc')

        if date_linked_to_ccc:
            date_linked_to_ccc = datetime.strptime(
                date_linked_to_ccc,  '%Y-%m-%d')
        name_specified = request.data.get('name_specified')
        client_ccc_number = request.data.get('client_ccc_number')
        number_of_sessions_attended = request.data.get(
            'number_of_sessions_attended')
        comment = request.data.get('comment')
        external_organization_other = request.data.get(
            'external_organization_other')

        intervention = {
            'intervention_date': intervention_date.date() if intervention_date else None,
            'client': client.id if client else None,
            'intervention_type': intervention_type.id if intervention_type else None,
            'name_specified': name_specified,
            'hts_result': hts_result.id if hts_result else None,
            'pregnancy_test_result': pregnancy_test_result.id if pregnancy_test_result else None,
            'client_ccc_number': client_ccc_number,
            'date_linked_to_ccc': date_linked_to_ccc.date() if date_linked_to_ccc else None,
            'number_of_sessions_attended': number_of_sessions_attended,
            'comment': comment,
            'created_by': created_by.id if created_by else None,
            'implementing_partner': implementing_partner.id if implementing_partner else None,
            'external_organization': external_organization.id if external_organization else None,
            'external_organization_other': external_organization_other,
            'date_created': datetime.now().date()
        }
        serializer = InterventionSerializer(data=intervention)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
