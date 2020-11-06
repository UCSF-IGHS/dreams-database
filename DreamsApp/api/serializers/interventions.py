from django.contrib.auth.models import User
from rest_framework import serializers

from DreamsApp.models import Intervention, HTSResult, InterventionType, PregnancyTestResult, ImplementingPartner, \
    ExternalOrganisation, Client


class InterventionSerializer(serializers.ModelSerializer):
    hts_result = serializers.SlugRelatedField(many=False, queryset=HTSResult.objects.all(), slug_field='code',
                                              read_only=False, allow_null=True)
    pregnancy_test_result = serializers.SlugRelatedField(many=False, queryset=PregnancyTestResult.objects.all(),
                                                         slug_field='code', read_only=False, allow_null=True)
    intervention_type = serializers.SlugRelatedField(many=False, queryset=InterventionType.objects.all(),
                                                     slug_field='code', read_only=False)
    implementing_partner = serializers.SlugRelatedField(many=False, queryset=ImplementingPartner.objects.all(),
                                                        slug_field='code', read_only=False)
    external_organisation = serializers.SlugRelatedField(many=False, queryset=ExternalOrganisation.objects.all(),
                                                         slug_field='code', read_only=False, allow_null=True)
    client = serializers.SlugRelatedField(many=False, queryset=Client.objects.all(), slug_field='id', read_only=False)
    created_by = serializers.SlugRelatedField(many=False, queryset=User.objects.all(), slug_field='username',
                                              read_only=False)

    class Meta:
        model = Intervention
        fields =(
            "intervention_date",
            "name_specified",
            "client_ccc_number",
            "date_linked_to_ccc",
            "no_of_sessions_attended",
            "date_created",
            "created_by",
            "hts_result",
            "client",
            "external_organisation",
            "pregnancy_test_result",
            "intervention_type",
            "implementing_partner"
        )


class InterventionListSerializer(serializers.ModelSerializer):
    hts_result = serializers.SlugRelatedField(many=False, queryset=HTSResult.objects.all(), slug_field='code',
                                              read_only=False, allow_null=True)
    pregnancy_test_result = serializers.SlugRelatedField(many=False, queryset=PregnancyTestResult.objects.all(),
                                                         slug_field='code', read_only=False, allow_null=True)
    intervention_type = serializers.SlugRelatedField(many=False, queryset=InterventionType.objects.all(),
                                                     slug_field='code', read_only=False)
    implementing_partner = serializers.SlugRelatedField(many=False, queryset=ImplementingPartner.objects.all(),
                                                        slug_field='code', read_only=False)
    external_organisation = serializers.SlugRelatedField(many=False, queryset=ExternalOrganisation.objects.all(),
                                                         slug_field='code', read_only=False, allow_null=True)
    client = serializers.SlugRelatedField(many=False, queryset=Client.objects.all(), slug_field='id', read_only=False)
    created_by = serializers.SlugRelatedField(many=False, queryset=User.objects.all(), slug_field='username',
                                              read_only=False)

    class Meta:
        model = Intervention
        fields = (
            "intervention_date",
            "name_specified",
            "client_ccc_number",
            "date_linked_to_ccc",
            "no_of_sessions_attended",
            "date_created",
            "created_by",
            "hts_result",
            "client",
            "external_organisation",
            "pregnancy_test_result",
            "intervention_type",
            "implementing_partner"
        )
