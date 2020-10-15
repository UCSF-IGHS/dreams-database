from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User
from DreamsApp.models import Intervention, Client, InterventionType, HTSResult, ExternalOrganisation, ImplementingPartner, PregnancyTestResult
from DreamsApp.serializers import InterventionSerializer


class InterventionCreateView(CreateAPIView):
    serializer_class = InterventionSerializer

    def perform_create(self, serializer):
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]
        data = JSONRenderer().render(serializer.validated_data)
        intervention_request = self.request.data
        try:
            client = Client.objects.get(pk=int(intervention_request['client']))
            created_by = User.objects.get(username=intervention_request['created_by'])
            hts_result = HTSResult.objects.get(code=intervention_request.get('hts_result'))

            intervention_type = InterventionType.objects.get(code=intervention_request['intervention_type'])
            external_organisation = intervention_request['external_organisation']
            if external_organisation:
                external_organisation = ExternalOrganisation.objects.get(code=external_organisation)

            pregnancy_test_result = intervention_request['pregnancy_test_result']
            if pregnancy_test_result:
                pregnancy_test_result = PregnancyTestResult.objects.get(code=pregnancy_test_result)
      
            implementing_partner = ImplementingPartner.objects.get(code=intervention_request['implementing_partner'])

            serializer.save(intervention_type=intervention_type, client = client, created_by=created_by, hts_result=hts_result, external_organisation=external_organisation, pregnancy_test_result=pregnancy_test_result, implementing_partner=implementing_partner)
            
        except User.DoesNotExist:
            return Response('The supplied user {} does not exist'.formart(intervention_request['created_by']))

        except HTSResult.DoesNotExist:
            return Response('The supplied HTSResult {} does not exist'.formart(intervention_request['hts_result']))
        
        except ExternalOrganisation.DoesNotExist:
            return Response('The supplied ExternalOrganization {} does not exist'.formart(intervention_request['external_organisation']))
        
        except PregnancyTestResult.DoesNotExist:
            return Response('The supplied PregnancyTestResult {} does not exist'.formart(intervention_request['pregnancy_result']))
        
        except ImplementingPartner.DoesNotExist:
            return Response('The supplied ImplementingPartner {} does not exist'.formart(intervention_request['implementing_partner']))
