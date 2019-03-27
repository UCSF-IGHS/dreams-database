from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from DreamsApp.models import *
from DreamsApp.constants import *


class FollowUpsServiceLayer:

    def __init__(self, user, follow_up=None):
        self.user: User = user
        self.followup: ClientFollowUp = follow_up

    def can_create_followup(self):
        return self.user is not None and self.user.is_superuser or self.user.has_perm('DreamsApp.add_clientfollowup')

    def can_delete_followup(self):
        return self.user is not None and self.user.is_superuser or self.user.has_perm('DreamsApp.delete_clientfollowup')

    def can_edit_followup(self):
        return self.user is not None and self.user.is_superuser or self.user.has_perm('DreamsApp.edit_clientfollowup')

    def can_view_followup(self):
        return self.user is not None and self.user.is_superuser or self.user.has_perm('DreamsApp.view_clientfollowup')


class TransferServiceLayer:

    def __init__(self, user, client_transfer=None):
        self.user: User = user
        self.client_transfer = client_transfer

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


class ClientEnrolmentServiceLayer:

    def __init__(self, user):
        self.user: User = user
        self.dt_format = "%Y-%m-%d"
        self.parameters = ConfigurableParameter.objects.all()
        self.ENROLMENT_CUTOFF_DATE = self.parameters.get(name='ENROLMENT_CUTOFF_DATE').value
        self.OLD_MINIMUM_ENROLMENT_AGE = self.parameters.get(name='OLD_MINIMUM_ENROLMENT_AGE').value
        self.NEW_MINIMUM_ENROLMENT_AGE = self.parameters.get(name='NEW_MINIMUM_ENROLMENT_AGE').value
        self.OLD_MAXIMUM_ENROLMENT_AGE = self.parameters.get(name='OLD_MAXIMUM_ENROLMENT_AGE').value
        self.NEW_MAXIMUM_ENROLMENT_AGE = self.parameters.get(name='NEW_MAXIMUM_ENROLMENT_AGE').value

    def get_minimum_maximum_enrolment_age(self, enrolment_cutoff_date):
        if datetime.now().date() >= datetime.strptime(str(enrolment_cutoff_date), self.dt_format).date():
            return [self.NEW_MINIMUM_ENROLMENT_AGE, self.NEW_MAXIMUM_ENROLMENT_AGE]
        else:
            return [self.OLD_MINIMUM_ENROLMENT_AGE, self.OLD_MAXIMUM_ENROLMENT_AGE]

    def is_within_enrolment_dates(self, date_of_birth, date_of_enrolment):
        date_of_birth = datetime.strptime(str(date_of_birth), self.dt_format).date()
        date_of_enrolment = datetime.strptime(str(date_of_enrolment), self.dt_format).date()
        enrolment_cutoff_age = self.get_minimum_maximum_enrolment_age(self.ENROLMENT_CUTOFF_DATE)

        max_dob = date_of_enrolment - relativedelta(years=int(enrolment_cutoff_age[0]))
        min_dob = date_of_enrolment - relativedelta(years=int(enrolment_cutoff_age[1]) + 1) + timedelta(days=1)
        return date_of_birth >= min_dob and date_of_birth <= max_dob


class ReferralServiceLayer:

    def __init__(self, user, client_referral=None):
        self.user: User = user
        self.client_referral = client_referral

    def can_accept_or_reject_referral(self):
        return self.user is not None and (self.user.is_superuser or self.user.has_perm('DreamsApp.change_referral'))

    def can_initiate_referral(self):
        return self.user is not None and (self.user.is_superuser or self.user.has_perm('DreamsApp.add_referral'))

    def can_complete_referral(self):
        action_allowed = False

        if self.user is not None and self.client_referral is not None:
            receiving_ip = self.client_referral.receiving_ip
            referring_ip = self.client_referral.referring_ip

            if self.client_referral.referral_status.pk == REFERRAL_PENDING_STATUS:
                if self.user.is_superuser:
                    action_allowed = True
                else:
                    user_ip = self.user.implementingpartneruser.implementing_partner
                    if self.user.has_perm('DreamsApp.change_referral') and (receiving_ip == user_ip or (referring_ip == user_ip and (self.client_referral.external_organisation or (
                            self.client_referral.external_organisation_other)))):
                        action_allowed = True

        return action_allowed

    def can_reject_referral(self):
        action_allowed = False

        if self.user is not None and self.client_referral is not None:
            receiving_ip = self.client_referral.receiving_ip
            referring_ip = self.client_referral.referring_ip

            if self.client_referral.referral_status.pk == REFERRAL_PENDING_STATUS:
                if self.user.is_superuser:
                    action_allowed = True
                else:
                    user_ip = self.user.implementingpartneruser.implementing_partner
                    if self.user.has_perm('DreamsApp.change_referral') and (receiving_ip == user_ip or (referring_ip == user_ip and (self.client_referral.external_organisation or (
                            self.client_referral.external_organisation_other)))):
                        action_allowed = True

        return action_allowed
