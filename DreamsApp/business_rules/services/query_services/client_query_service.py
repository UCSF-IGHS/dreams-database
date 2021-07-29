from datetime import datetime

from django.db.models import Q

from DreamsApp.exceptions import ClientSearchException
from DreamsApp.models import Client, ServiceDelegation


class ClientQueryService:

    def __init__(self, user):
        self.user = user

    def get_clients(self):
        if self.user:
            ## EXCLUDE DELEGATION
            # clients = Client.objects.select_related('implementing_partner', 'ward', 'ward__sub_county',
            #                                         'ward__sub_county__county')

            # delegating_ips = self._get_delegating_ips()
            # clients = clients.filter(
            #     (Q(implementing_partner__in=delegating_ips) | Q(implementing_partner=self.user.implementing_partner))
            #     & Q(voided=False))

            # clients = Client.objects.select_related('implementing_partner', 'ward', 'ward__sub_county',
            #                                         'ward__sub_county__county').filter(
            #     (Q(implementing_partner=self.user.implementing_partner))
            #     & Q(voided=False))

            clients = Client.objects.filter(
                (Q(implementing_partner=self.user.implementing_partner))
                & Q(voided=False))
            return clients

    def get_client(self, dreams_id):
        ## EXCLUDE DELEGATION
        # clients = self.get_clients()
        # return clients.get(dreams_id=dreams_id)
        return Client.objects.get(dreams_id=dreams_id)

    def search_clients(self, search_criteria):
        clients = self.get_clients()
        if 'search_text' in search_criteria:
            clients = self._filter_clients_by_search_term(clients, search_criteria['search_text'])
        if 'enrolment_start_date' in search_criteria:
            clients = clients.filter(date_of_enrollment__gte=search_criteria['enrolment_start_date'])
        if 'enrolment_end_date' in search_criteria:
            clients = clients.filter(date_of_enrollment__lte=search_criteria['enrolment_end_date'])
        if 'ward' in search_criteria:
            clients = clients.filter(ward=search_criteria['ward'])
        elif 'sub_county' in search_criteria:
            clients = clients.filter(ward__sub_county=search_criteria['sub_county'])
        if 'county' in search_criteria:
            clients = clients.filter(ward__sub_county__county=search_criteria['county'])
        if clients.exists():
            return clients
        raise Client.DoesNotExist

    def _get_delegating_ips(self):
        delegations = ServiceDelegation.objects.filter(delegated_implementing_partner=self.user.implementing_partner,
                                                       start_date__lte=datetime.now().date(),
                                                       end_date__gte=datetime.now().date())
        delegating_ips = [delegation.main_implementing_partner for delegation in delegations]
        return delegating_ips

    def _filter_clients_by_search_term(self, clients, search_text):
        search_terms = search_text.split()

        if len(search_terms) > 1:
            clients = self._build_filter_client_queryset(clients, search_terms)
        else:
            clients = self._build_filter_client_queryset_for_one_word_search_text(clients, search_terms)
        return clients

    def _build_filter_client_queryset(self, clients, search_terms):
        try:
            if len(search_terms) == 2:
                search_terms.append('')

            clients = clients.filter(
                Q(first_name__icontains=str(search_terms[0]), middle_name__icontains=str(search_terms[1]),
                  last_name__icontains=str(search_terms[2])) | Q(first_name__icontains=str(search_terms[0]),
                                                                 middle_name__icontains=str(search_terms[2]),
                                                                 last_name__icontains=str(search_terms[1])) | Q(
                    first_name__icontains=str(search_terms[1]), middle_name__icontains=str(search_terms[0]),
                    last_name__icontains=str(search_terms[2])) | Q(first_name__icontains=str(search_terms[1]),
                                                                   middle_name__icontains=str(search_terms[2]),
                                                                   last_name__icontains=str(search_terms[0])) | Q(
                    first_name__icontains=str(search_terms[2]), middle_name__icontains=str(search_terms[0]),
                    last_name__icontains=str(search_terms[1])) | Q(first_name__icontains=str(search_terms[2]),
                                                                   middle_name__icontains=str(search_terms[1]),
                                                                   last_name__icontains=str(search_terms[0])) | Q(
                    first_name__icontains=str(search_terms[0] + ' ' + search_terms[1]),
                    middle_name__icontains=str(search_terms[2]))
                | Q(
                    first_name__icontains=str(search_terms[0] + ' ' + search_terms[1]),
                    last_name__icontains=str(search_terms[2])) | Q(
                    first_name__icontains=str(search_terms[0] + ' ' + search_terms[1]),
                    middle_name__icontains=str(search_terms[2])) | Q(
                    middle_name__icontains=str(search_terms[0] + ' ' + search_terms[1]),
                    first_name__icontains=str(search_terms[2])) | Q(
                    middle_name__icontains=str(search_terms[0] + ' ' + search_terms[1]),
                    last_name__icontains=str(search_terms[2])) | Q(
                    last_name__icontains=str(search_terms[0] + ' ' + search_terms[1]),
                    first_name__icontains=str(search_terms[2])) | Q(
                    last_name__icontains=str(search_terms[0] + ' ' + search_terms[1]),
                    middle_name__icontains=str(search_terms[2])) | Q(
                    first_name__icontains=str(search_terms[0] + ' ' + search_terms[2]),
                    last_name__icontains=str(search_terms[1])) | Q(
                    first_name__icontains=str(search_terms[0] + ' ' + search_terms[2]),
                    middle_name__icontains=str(search_terms[1])) | Q(
                    middle_name__icontains=str(search_terms[0] + ' ' + search_terms[2]),
                    first_name__icontains=str(search_terms[1])) | Q(
                    middle_name__icontains=str(search_terms[0] + ' ' + search_terms[2]),
                    last_name__icontains=str(search_terms[1])) | Q(
                    last_name__icontains=str(search_terms[0] + ' ' + search_terms[2]),
                    first_name__icontains=str(search_terms[1])) | Q(
                    last_name__icontains=str(search_terms[0] + ' ' + search_terms[2]),
                    middle_name__icontains=str(search_terms[1]))

                | Q(
                    first_name__icontains=str(search_terms[1] + ' ' + search_terms[0]),
                    last_name__icontains=str(search_terms[2])) | Q(
                    first_name__icontains=str(search_terms[1] + ' ' + search_terms[2]),
                    middle_name__icontains=str(search_terms[0])) | Q(
                    middle_name__icontains=str(search_terms[1] + ' ' + search_terms[0]),
                    first_name__icontains=str(search_terms[2])) | Q(
                    middle_name__icontains=str(search_terms[1] + ' ' + search_terms[2]),
                    last_name__icontains=str(search_terms[0])) | Q(
                    last_name__icontains=str(search_terms[1] + ' ' + search_terms[0]),
                    first_name__icontains=str(search_terms[2])) | Q(
                    last_name__icontains=str(search_terms[1] + ' ' + search_terms[2]),
                    middle_name__icontains=str(search_terms[0])) | Q(
                    first_name__icontains=str(search_terms[1] + ' ' + search_terms[0]),
                    last_name__icontains=str(search_terms[2])) | Q(
                    first_name__icontains=str(search_terms[1] + ' ' + search_terms[2]),
                    middle_name__icontains=str(search_terms[0])) | Q(
                    middle_name__icontains=str(search_terms[1] + ' ' + search_terms[0]),
                    first_name__icontains=str(search_terms[2])) | Q(
                    middle_name__icontains=str(search_terms[1] + ' ' + search_terms[2]),
                    last_name__icontains=str(search_terms[0])) | Q(
                    last_name__icontains=str(search_terms[1] + ' ' + search_terms[0]),
                    first_name__icontains=str(search_terms[2])) | Q(
                    last_name__icontains=str(search_terms[1] + ' ' + search_terms[2]),
                    middle_name__icontains=str(search_terms[0]))

                | Q(
                    first_name__icontains=str(search_terms[2] + ' ' + search_terms[0]),
                    last_name__icontains=str(search_terms[1])) | Q(
                    first_name__icontains=str(search_terms[2] + ' ' + search_terms[1]),
                    middle_name__icontains=str(search_terms[0])) | Q(
                    middle_name__icontains=str(search_terms[2] + ' ' + search_terms[0]),
                    first_name__icontains=str(search_terms[1])) | Q(
                    middle_name__icontains=str(search_terms[2] + ' ' + search_terms[1]),
                    last_name__icontains=str(search_terms[0])) | Q(
                    last_name__icontains=str(search_terms[2] + ' ' + search_terms[0]),
                    first_name__icontains=str(search_terms[1])) | Q(
                    last_name__icontains=str(search_terms[2] + ' ' + search_terms[1]),
                    middle_name__icontains=str(search_terms[0])) | Q(
                    first_name__icontains=str(search_terms[2] + ' ' + search_terms[0]),
                    last_name__icontains=str(search_terms[1])) | Q(
                    first_name__icontains=str(search_terms[2] + ' ' + search_terms[1]),
                    middle_name__icontains=str(search_terms[0])) | Q(
                    middle_name__icontains=str(search_terms[2] + ' ' + search_terms[0]),
                    first_name__icontains=str(search_terms[1])) | Q(
                    middle_name__icontains=str(search_terms[2] + ' ' + search_terms[1]),
                    last_name__icontains=str(search_terms[0])) | Q(
                    last_name__icontains=str(search_terms[2] + ' ' + search_terms[0]),
                    first_name__icontains=str(search_terms[1])) | Q(
                    last_name__icontains=str(search_terms[2] + ' ' + search_terms[1]),
                    middle_name__icontains=str(search_terms[0])) | self._conditional_filter(search_terms)
            )

            return clients

        except Exception as e:
            message = e.message if hasattr(e, 'message') else ''
            raise ClientSearchException(
                message='Error encountered when searching for client with the provided search terms. {}'.format(
                    message))

    def _conditional_filter(self, search_terms):
        if search_terms[2] == '':
            return Q(
                first_name__icontains=str(search_terms[0] + ' ' + search_terms[1])) | Q(
                first_name__icontains=str(search_terms[1] + ' ' + search_terms[0])) | Q(
                middle_name__icontains=str(search_terms[0] + ' ' + search_terms[1])) | Q(
                middle_name__icontains=str(search_terms[1] + ' ' + search_terms[0])) | Q(
                last_name__icontains=str(search_terms[0] + ' ' + search_terms[1])) | Q(
                last_name__icontains=str(search_terms[1] + ' ' + search_terms[0]))
        else:
            return Q()

    def _build_filter_client_queryset_for_one_word_search_text(self, clients, search_terms):
        try:
            clients = clients.filter(
                Q(first_name__icontains=str(search_terms[0])) | Q(first_name=str(search_terms[0])) | Q(
                    middle_name__icontains=str(search_terms[0])) | Q(middle_name=str(search_terms[0])) | Q(
                    last_name__icontains=str(search_terms[0])) | Q(last_name=str(search_terms[0])) | Q(dreams_id=str(search_terms[0])))

            return clients

        except Exception as e:
            message = str(e)
            raise ClientSearchException(
                message='Error encountered when searching for client with the provided search terms. {}'.format(
                    message))
