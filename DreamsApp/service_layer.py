
from django.contrib.auth.models import User
from DreamsApp.models import *


TRANSFER_INITIATED_STATUS = 1
TRANSFER_ACCEPTED_STATUS = 2

class FollowUpsServiceLayer:

    def __init__(self, user, follow_up=None):
        self.user: User = user
        self.followup: ClientFollowUp = follow_up


    def can_create_followup(self):
        return self.user is not None and self.user.is_superuser or self.user.has_perm('DreamsApp.add_followup')

    def can_delete_followup(self):
        return self.user is not None and self.user.is_superuser or self.user.has_perm('DreamsApp.delete_followup')

    def can_edit_followup(self):
        return self.user is not None and self.user.is_superuser or self.user.has_perm('DreamsApp.edit_followup')


class TransferServiceLayer:
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

            if self.client_transfer.transfer_status.pk == TRANSFER_INITIATED_STATUS:
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

            if self.client_transfer.transfer_status.pk == TRANSFER_INITIATED_STATUS:
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

            if self.client_transfer.transfer_status.pk == TRANSFER_ACCEPTED_STATUS:
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
