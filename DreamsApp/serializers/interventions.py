from rest_framework import serializers
from DreamsApp.models import Intervention


class InterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervention
        fields = ('client', 'intervention_date', 'intervention_type', 'name_specified', 'hts_result',
                  'client_ccc_number', 'date_linked_to_ccc', 'no_of_sessions_attended', 'implementing_partner', 'created_by', 'date_created')
