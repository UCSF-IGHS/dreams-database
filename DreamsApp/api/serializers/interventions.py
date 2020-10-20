from rest_framework import serializers
from DreamsApp.models import Intervention


class InterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervention
        fields = (
            'intervention_date',  'name_specified',
            'client_ccc_number', 'date_linked_to_ccc', 'no_of_sessions_attended', 'date_created'
        )


class InterventionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervention
        fields = (
            'intervention_date',  'name_specified',
            'client_ccc_number', 'date_linked_to_ccc', 'no_of_sessions_attended', 'date_created',
            'created_by', 'hts_result', 'client', 'pregnancy_test_result', 'intervention_type',
            'implementing_partner'
        )
