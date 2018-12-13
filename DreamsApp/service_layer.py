
from django.contrib.auth.models import User
from DreamsApp.models import *


class TransferServiceLayer:
    def __init__(self, user, transfer_type=None, client_transfer=None):
        self.user: User = user
        self.transfer_type = transfer_type
        self.client_transfer: ClientTransfer = client_transfer

    def can_initiate_transfer(self):
        action_allowed = False
        #user_ip = self.user.implementingpartneruser.implementing_partner

        if self.user.is_superuser or self.user.has_perm('DreamsApp.add_clienttransfer'):
            action_allowed = True

        return action_allowed

    def can_accept_or_reject_transfer(self):
        action_allowed = False

        if self.user is not None:
            if self.user.is_superuser:
                action_allowed = True
            else:
                if self.client_transfer is not None:
                    user_ip = self.user.implementingpartneruser.implementing_partner
                    source_ip = self.client_transfer.source_implementing_partner
                    destination_ip = self.client_transfer.destination_implementing_partner
                    initiated_transfer_status = ClientTransferStatus.objects.get(code__exact=1)

                    if self.client_transfer.transfer_status == initiated_transfer_status:
                        if self.user.has_perm('DreamsApp.change_clienttransfer'):
                            if self.transfer_type == "transferred_in" and destination_ip == user_ip:
                                action_allowed = True

        return action_allowed

    def can_complete_transfer(self):
        action_allowed = False

        if self.user is not None:
            action_allowed = True
        else:
            if self.client_transfer is not None:
                user_ip = self.user.implementingpartneruser.implementing_partner
                source_ip = self.client_transfer.source_implementing_partner
                destination_ip = self.client_transfer.destination_implementing_partner
                accepted_transfer_status = ClientTransferStatus.objects.get(code__exact=2)

                if self.client_transfer.transfer_status == accepted_transfer_status:
                    if self.user.has_perm('DreamsApp.change_clienttransfer'):
                        if self.transfer_type == "transferred_in" and destination_ip == user_ip:
                            action_allowed = True

        return action_allowed
