
from django.contrib.auth.models import User
from DreamsApp.models import *


TRANSFER_INITIATED_STATUS = 1
TRANSFER_ACCEPTED_STATUS = 2


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
            initiated_transfer_status = ClientTransferStatus.objects.get(code__exact=TRANSFER_INITIATED_STATUS)

            if self.client_transfer.transfer_status == initiated_transfer_status:
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
            initiated_transfer_status = ClientTransferStatus.objects.get(code__exact=TRANSFER_INITIATED_STATUS)

            if self.client_transfer.transfer_status == initiated_transfer_status:
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
            initiated_transfer_status = ClientTransferStatus.objects.get(code__exact=TRANSFER_ACCEPTED_STATUS)

            if self.client_transfer.transfer_status == initiated_transfer_status:
                if self.user.is_superuser:
                    action_allowed = True
                else:
                    user_ip = self.user.implementingpartneruser.implementing_partner
                    if self.user.has_perm('DreamsApp.change_clienttransfer') and destination_ip == user_ip:
                        action_allowed = True

        return action_allowed
