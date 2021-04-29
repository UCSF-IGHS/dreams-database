from django.db.models import Q

from DreamsApp.models import Intervention


class InterventionQueryService:

    def __init__(self, user):
        self.user = user

    def get_interventions(self):
        if self.user is not None :
            interventions = Intervention.objects.select_related('client', 'intervention_type')
            interventions = interventions.filter(~Q(voided=True), ~Q(client__voided=True))
            interventions = interventions.filter(Q(implementing_partner=self.user.implementing_partner) | Q(
                client__implementing_partner=self.user.implementing_partner) | Q(
                client__implementing_partner__in=self.user.implementing_partner.get_active_delegating_implementing_partners))

            return interventions

    def get_interventions_for_client(self, client = None):
        return Intervention.objects.none()