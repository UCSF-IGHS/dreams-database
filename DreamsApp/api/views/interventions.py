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
from DreamsApp.models import (
    Intervention,
    Client,
    InterventionType,
    HTSResult,
    ExternalOrganisation,
    ImplementingPartner,
    PregnancyTestResult,
)
from DreamsApp.api.serializers import InterventionSerializer, InterventionListSerializer


class InterventionCreateView(CreateAPIView):
    serializer_class = InterventionSerializer

    def perform_create(self, serializer):
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]
        data = JSONRenderer().render(serializer.validated_data)
        intervention_request = self.request.data
        try:
            client = Client.objects.get(pk=int(intervention_request["client"]))
            created_by = User.objects.get(username=intervention_request["created_by"])
            hts_result = HTSResult.objects.get(
                code=intervention_request.get("hts_result")
            )

            intervention_type = InterventionType.objects.get(
                code=intervention_request["intervention_type"]
            )
            external_organisation = intervention_request["external_organisation"]
            if external_organisation:
                external_organisation = ExternalOrganisation.objects.get(
                    code=external_organisation
                )

            pregnancy_test_result = intervention_request["pregnancy_test_result"]
            if pregnancy_test_result:
                pregnancy_test_result = PregnancyTestResult.objects.get(
                    code=pregnancy_test_result
                )

            implementing_partner = ImplementingPartner.objects.get(
                code=intervention_request["implementing_partner"]
            )

            serializer.save(
                intervention_type=intervention_type,
                client=client,
                created_by=created_by,
                hts_result=hts_result,
                external_organisation=external_organisation,
                pregnancy_test_result=pregnancy_test_result,
                implementing_partner=implementing_partner,
            )

            # respond wit

        except User.DoesNotExist:
            # do a 405 bad request
            return Response(
                status=404,
                data={
                    "message": "The supplied user {} does not exist".formart(
                        intervention_request["created_by"]
                    )
                },
            )

        except HTSResult.DoesNotExist:
            return Response(
                status=404,
                data={
                    "message": "The supplied HTSResult {} does not exist".formart(
                        intervention_request["hts_result"]
                    )
                },
            )

        except ExternalOrganisation.DoesNotExist:
            return Response(
                status=404,
                data={
                    "message": "The supplied ExternalOrganization {} does not exist".formart(
                        intervention_request["external_organisation"]
                    )
                },
            )

        except PregnancyTestResult.DoesNotExist:
            return Response(
                status=404,
                data={
                    "message": "The supplied PregnancyTestResult {} does not exist".formart(
                        intervention_request["pregnancy_result"]
                    )
                },
            )

        except ImplementingPartner.DoesNotExist:
            return Response(
                status=404,
                data={
                    "message": "The supplied ImplementingPartner {} does not exist".formart(
                        intervention_request["implementing_partner"]
                    )
                },
            )


class InterventionMultipleCreateView(CreateAPIView):
    serializer_class = InterventionListSerializer

    def post(self, request):
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]

        try:
            interventions = self.request.data
            if not self.request.data:
                return Response(
                    status=400, data={"message": "The request body was empty"}
                )
            for intervention in interventions:
                try:
                    client = Client.objects.get(pk=int(intervention["client"]))
                    intervention["client"] = client.id
                    created_by = User.objects.get(username=intervention["created_by"])
                    intervention["created_by"] = created_by.id

                    hts_result = intervention["hts_result"]
                    if hts_result:
                        hts_result = HTSResult.objects.get(
                            code=intervention["hts_result"]
                        )
                        intervention["hts_result"] = hts_result.id

                    intervention_type = intervention["intervention_type"]
                    if intervention_type:
                        intervention_type = InterventionType.objects.get(
                            code=intervention["intervention_type"]
                        )
                        intervention["intervention_type"] = intervention_type.id

                    external_organisation = intervention["external_organisation"]
                    if external_organisation:
                        external_organisation = ExternalOrganisation.objects.get(
                            code=external_organisation
                        )
                        intervention["external_organisation"] = external_organisation.id

                    pregnancy_test_result = intervention["pregnancy_test_result"]
                    if pregnancy_test_result:
                        pregnancy_test_result = PregnancyTestResult.objects.get(
                            code=pregnancy_test_result
                        )
                        intervention["pregnancy_test_result"] = pregnancy_test_result.id

                    implementing_partner = intervention["implementing_partner"]
                    if implementing_partner:
                        implementing_partner = ImplementingPartner.objects.get(
                            code=intervention["implementing_partner"]
                        )
                        intervention["implementing_partner"] = implementing_partner.id

                except User.DoesNotExist:
                    return Response(
                        status=404,
                        data={
                            "message": "The supplied user {} does not exist".format(
                                intervention["created_by"]
                            )
                        },
                    )

                except Client.DoesNotExist:
                    return Response(
                        status=404,
                        data={
                            "message": "The supplied client {} does not exist".format(
                                intervention["client"]
                            )
                        },
                    )

                except HTSResult.DoesNotExist:
                    return Response(
                        status=404,
                        data={
                            "message": "The supplied HTSResult {} does not exist".format(
                                intervention["hts_result"]
                            )
                        },
                    )

                except ExternalOrganisation.DoesNotExist:
                    return Response(
                        status=404,
                        data={
                            "message": "The supplied ExternalOrganization {} does not exist".format(
                                intervention["external_organisation"]
                            )
                        },
                    )

                except PregnancyTestResult.DoesNotExist:
                    return Response(
                        status=404,
                        data={
                            "message": "The supplied PregnancyTestResult {} does not exist".format(
                                intervention["pregnancy_test_result"]
                            )
                        },
                    )

                except ImplementingPartner.DoesNotExist:
                    return Response(
                        status=404,
                        data={
                            "message": "The supplied ImplementingPartner {} does not exist".format(
                                intervention["implementing_partner"]
                            )
                        },
                    )
            serializer = InterventionListSerializer(data=interventions, many=True)
            if serializer.is_valid():
                serializer.save()

            return Response(
                status=201, data={"message": "Success! Records successfully created"}
            )

        except Exception:
            return Response(status=500, data={"message": "Internal Server Error"})
