from django.db.models import Q

from DreamsApp.models import Client, ServiceDelegation, Intervention


class ClientQueryService:

    def __init__(self, user):
        self.user = user

    def get_clients(self):
        if self.user:
            clients = Client.objects.select_related('implementing_partner', )
            delegating_ips = self._get_delegating_ips()
            intervention_clients = self._get_intervention_clients()
            clients = clients.filter(
                Q(implementing_partner__in=delegating_ips) | Q(implementing_partner=self.user.implementing_partner) | Q(
                    id__in=intervention_clients))
            return clients

    def _get_delegating_ips(self):
        delegations = ServiceDelegation.objects.filter(delegated_implementing_partner=self.user.implementing_partner)
        delegating_ips = [delegation.main_implementing_partner for delegation in delegations]
        return delegating_ips

    def _get_intervention_clients(self):
        intervention_queryset = Intervention.objects.select_related('client')
        intervention_queryset = intervention_queryset.filter(implementing_partner=self.user.implementing_partner).filter(
            ~Q(client__implementing_partner=self.user.implementing_partner)).only('client').distinct()
        return [intervention.client.id for intervention in intervention_queryset]
