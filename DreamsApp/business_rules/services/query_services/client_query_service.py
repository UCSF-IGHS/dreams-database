from datetime import datetime

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
                Q(implementing_partner__in=delegating_ips) | Q(implementing_partner=self.user.implementing_partner))
            clients = clients.filter(voided=False)
            clients = clients | intervention_clients
            return clients

    def get_client(self, dreams_id):
        clients = self.get_clients()
        return clients.get(dreams_id=dreams_id)

    def _get_delegating_ips(self):
        delegations = ServiceDelegation.objects.filter(delegated_implementing_partner=self.user.implementing_partner,
                                                       start_date__lte=datetime.now().date(),
                                                       end_date__gte=datetime.now().date())
        delegating_ips = [delegation.main_implementing_partner for delegation in delegations]
        return delegating_ips

    def _get_intervention_clients(self):
        interventions = Intervention.objects.select_related('client')
        client_ids = interventions.filter(implementing_partner=self.user.implementing_partner, voided=False,
                                          client__voided=False)
        client_ids = client_ids.filter(
            ~Q(client__implementing_partner=self.user.implementing_partner)).values('client_id').distinct()

        clients = Client.objects.filter(id__in=client_ids).select_related('implementing_partner')
        return clients
