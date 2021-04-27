from django.db.models import Q

from DreamsApp.models import Intervention


class InterventionQueryService:

    def __init__(self, user):
        self.user = user

    def get_interventions(self):
        if self.user:
            test_i = Intervention.objects.filter(implementing_partner_id=4)
            interventions = Intervention.objects.select_related('client', 'intervention_type')
            interventions = interventions.filter(~Q(voided=True), ~Q(client__voided=True))
            interventions = interventions.filter(Q(implementing_partner=self.user.implementing_partner) | Q(
                client__implementing_partner=self.user.implementing_partner) | Q(
                client__implementing_partner__in=self.user.implementing_partner.get_delegating_implementing_partners))

            return interventions
