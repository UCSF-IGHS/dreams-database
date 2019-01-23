
from django.contrib.auth.models import User
from DreamsApp.models import *


class TransferServiceLayer:
    TRANSFER_INITIATED_STATUS = 1
    TRANSFER_ACCEPTED_STATUS = 2
    TRANSFER_REJECTED_STATUS = 3

    def __init__(self, user, client_transfer=None):
        self.user: User = user
        self.client_transfer: ClientTransfer = client_transfer

    def can_initiate_transfer(self):
        if self.user is not None:
            return self.user.is_superuser or self.user.has_perm('DreamsApp.add_clienttransfer')
        else:
            return False

    def can_accept_or_reject_transfer(self):
        if self.user is not None:
            return self.user.is_superuser or self.user.has_perm('DreamsApp.change_clienttransfer')
        else:
            return False

    def can_accept_transfer(self):
        action_allowed = False

        if self.user is not None and self.client_transfer is not None:
            destination_ip = self.client_transfer.destination_implementing_partner

            if self.client_transfer.transfer_status.pk == self.TRANSFER_INITIATED_STATUS:
                if self.user.is_superuser:
                    action_allowed = True
                else:
                    user_ip = self.user.implementingpartneruser.implementing_partner
                    if self.user.has_perm('DreamsApp.change_clienttransfer') and destination_ip == user_ip:
                        action_allowed = True

        return action_allowed

    def can_reject_transfer(self):
        action_allowed = False

        if self.user is not None and self.client_transfer is not None:
            destination_ip = self.client_transfer.destination_implementing_partner

            if self.client_transfer.transfer_status.pk == self.TRANSFER_INITIATED_STATUS:
                if self.user.is_superuser:
                    action_allowed = True
                else:
                    user_ip = self.user.implementingpartneruser.implementing_partner
                    if self.user.has_perm('DreamsApp.change_clienttransfer') and destination_ip == user_ip:
                        action_allowed = True

        return action_allowed

    def can_complete_transfer(self):
        action_allowed = False

        if self.user is not None and self.client_transfer is not None:
            destination_ip = self.client_transfer.destination_implementing_partner

            if self.client_transfer.transfer_status.pk == self.TRANSFER_ACCEPTED_STATUS:
                if self.user.is_superuser:
                    action_allowed = True
                else:
                    user_ip = self.user.implementingpartneruser.implementing_partner
                    if self.user.has_perm('DreamsApp.change_clienttransfer') and destination_ip == user_ip:
                        action_allowed = True

        return action_allowed

    def client_transfer_status(self, user_ip, client, implementing_partner_query, transfer_status):
        try:
            clients_transferred = client.clienttransfer_set.filter(client_id=client.pk).order_by('-id')
            if clients_transferred.exists():
                client_transfer_found = clients_transferred.first()

                if implementing_partner_query == "source_implementing_partner":
                    return client_transfer_found.transfer_status.pk == transfer_status if client_transfer_found.source_implementing_partner == user_ip else False

                elif implementing_partner_query == "destination_implementing_partner":
                    return client_transfer_found.transfer_status.pk == transfer_status if client_transfer_found.destination_implementing_partner == user_ip else False

            return False
        except:
            return False


class ClientEnrolmentServiceLayer:
    MINIMUM_ENROLMENT_AGE = 9
    MAXIMUM_ENROLMENT_AGE = 24

    def __init__(self, user):
        self.user: User = user
        self.dt_format = "%Y-%m-%d"

    def is_within_enrolment_dates(self, date_of_birth):
        max_dob = datetime.now().replace(year=datetime.now().year - self.MINIMUM_ENROLMENT_AGE).strftime(self.dt_format)
        min_dob = datetime.now().replace(year=datetime.now().year - self.MAXIMUM_ENROLMENT_AGE).strftime(self.dt_format)
        return True if date_of_birth >= min_dob or date_of_birth <= max_dob else False
