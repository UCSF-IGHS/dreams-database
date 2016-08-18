# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class MaritalStatus(models.Model):
    code = models.CharField(verbose_name='Marital Status Code', max_length=10, null=False, blank=False)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Marital Status'
        verbose_name_plural = 'Marital Status'


class County(models.Model):
    code = models.CharField(verbose_name='County Code', max_length=10, default='', null=False, blank=False)
    name = models.CharField(verbose_name='County', max_length=100, default='', null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'County'
        verbose_name_plural = 'Counties'


class SubCounty(models.Model):
    county = models.ForeignKey(County, null=True, blank=True)
    code = models.CharField(verbose_name='Sub County Code', max_length=100, default='', null=False, blank=False)
    name = models.CharField(verbose_name='Sub County', max_length=100, default='', null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Sub County'
        verbose_name_plural = 'Sub Counties'


class Ward(models.Model):
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True)
    code = models.CharField(verbose_name='Ward Code', max_length=100, default='', null=False, blank=False)
    name = models.CharField(verbose_name='Ward', max_length=100, default='', null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Ward'
        verbose_name_plural = 'Wards'


class VerificationDocument(models.Model):
    code = models.IntegerField(name='code', verbose_name='Verification Document Code')
    name = models.CharField(max_length=150, verbose_name='Verification Document Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Verification Document'
        verbose_name_plural = 'Verification Documents'


class ImplementingPartner(models.Model):
    code = models.IntegerField(name='code', verbose_name='Implementing Partner Code')
    name = models.CharField(max_length=150, verbose_name='Implementing Partner Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Implementing Partner'
        verbose_name_plural = 'Implementing Partners'


class ImplementingPartnerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    implementing_partner = models.ForeignKey(ImplementingPartner, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    class Meta(object):
        verbose_name = 'Implementing Partner User'
        verbose_name_plural = 'Implementing Partner Users'


class Client(models.Model):
    first_name = models.CharField(verbose_name='First Name', max_length=100, null=True)
    middle_name = models.CharField(verbose_name='Middle Name', max_length=100, null=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=100, null=True)
    date_of_birth = models.DateField(verbose_name='Date Of Birth', null=True)
    is_date_of_birth_estimated = models.BooleanField(verbose_name='Date of Birth Estimated')
    verification_document = models.ForeignKey(VerificationDocument, null=True, blank=True)  # New
    verification_doc_no = models.CharField(verbose_name='Verification Doc. No.', max_length=50, null=True)
    date_of_enrollment = models.DateField(verbose_name='Date of Enrollment', default=datetime.now, null=True)
    age_at_enrollment = models.IntegerField(verbose_name='Age at Enrollment', default=10, null=True)
    marital_status = models.ForeignKey(MaritalStatus, verbose_name='Marital Status', null=True)

    implementing_partner = models.ForeignKey(ImplementingPartner, null=True, blank=True)  # New

    phone_number = models.CharField(verbose_name='Phone Number(Client)', max_length=13, null=True)
    dss_id_number = models.CharField(verbose_name='DSS ID Number', max_length=50, null=True)
    county_of_residence = models.ForeignKey(County, verbose_name='County of residence', null=True)
    sub_county = models.ForeignKey(SubCounty, verbose_name='Sub County', null=True)
    ward = models.ForeignKey(Ward, verbose_name='Ward', null=True)
    informal_settlement = models.CharField(verbose_name='Informal Settlement', max_length=250, null=True)
    village = models.CharField(verbose_name='Village', max_length=250, null=True)
    landmark = models.CharField(verbose_name='Land mark near residence', max_length=250, null=True)
    dreams_id = models.CharField(verbose_name='DREAMS ID', max_length=50, null=True)
    guardian_name = models.CharField(verbose_name='Primary care give / Guardian\' name', max_length=250, null=True)
    relationship_with_guardian = models.CharField(verbose_name='Relationship with Guardian', max_length=50, null=True)
    guardian_phone_number = models.CharField(verbose_name='Phone Number(Care giver / Guardian)', max_length=13,
                                             null=True)
    guardian_national_id = models.CharField(verbose_name='National ID (Care giver / Guardian)', max_length=10,
                                            null=True)

    enrolled_by = models.ForeignKey(User, null=True)

    def save(self, user_id=None, action=None, *args, **kwargs):  # pass audit to args as the first object
        super(Client, self).save(*args, **kwargs)
        if user_id is None:
            return
        audit = Audit()
        audit.user_id = user_id
        audit.table = "DreamsApp_client"
        audit.row_id = self.pk
        audit.action = action
        audit.search_text = None
        audit.save()

    def __str__(self):
        return '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)

    def get_full_name(self):
        try:
            f_name = '' if not self.first_name else self.first_name
            m_name = ' ' if not self.middle_name else self.middle_name
            l_name = ' ' if not self.last_name else self.last_name
            return f_name + ' ' + m_name + ' ' + l_name
        except:
            return "Invalid Client Name"

    def get_age_at_enrollment(self):
        try:
            return self.date_of_enrollment.year - self.date_of_birth.year - (
                (self.date_of_enrollment.month, self.date_of_enrollment.day) < (
                    self.date_of_birth.month, self.date_of_birth.day))
        except:
            return 10

    def get_current_age(self):
        try:
            return datetime.now().year - self.date_of_birth.year - (
                (datetime.now().month, datetime.now().day) < (
                    self.date_of_birth.month, self.date_of_birth.day))
        except:
            return 10

    class Meta(object):
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class InterventionCategory(models.Model):
    code = models.IntegerField(verbose_name='Intervention Category Code', default=0)
    name = models.CharField(max_length=30)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Intervention Category'
        verbose_name_plural = 'Intervention Categories'


class InterventionType(models.Model):
    code = models.IntegerField(verbose_name='Intervention Type Code', default=0, null=False, blank=False)
    name = models.CharField(max_length=100, null=False)
    intervention_category = models.ForeignKey(InterventionCategory, null=False, blank=False)
    has_hts_result = models.BooleanField(default=False, verbose_name='Intervention collects HTS Result')
    has_pregnancy_result = models.BooleanField(default=False, verbose_name='Intervention collects Pregnancy Result')
    has_ccc_number = models.BooleanField(default=False, verbose_name='Intervention collects CCC details')
    has_no_of_sessions = models.BooleanField(default=False, verbose_name='Intervention collects No. of sessions')
    min_age = models.IntegerField(verbose_name='Minimum AGYW Age', default=0, null=False, blank=False)
    max_age = models.IntegerField(verbose_name='Maximum AGYW Age', default=0, null=False, blank=False)
    is_age_restricted = models.BooleanField(default=False, verbose_name='Intervention is Age Restricted')
    is_given_once = models.BooleanField(default=False, verbose_name='Intervention is given Once')
    is_specified = models.BooleanField(default=False, verbose_name='Intervention is specified')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Intervention Type'
        verbose_name_plural = 'Intervention Types'


class HTSResult(models.Model):
    code = models.IntegerField(name='code', verbose_name='HTS Result Code')
    name = models.CharField(max_length=20, verbose_name='HTS Result Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'HTS Result'
        verbose_name_plural = 'HTS Results'


class PregnancyTestResult(models.Model):
    code = models.IntegerField(name='code', verbose_name='Pregnancy Result Code')
    name = models.CharField(max_length=20, verbose_name='Pregnancy Result Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Pregnancy Result'
        verbose_name_plural = 'Pregnancy Results'


class Intervention(models.Model):
    intervention_date = models.DateField()
    client = models.ForeignKey(Client)
    intervention_type = models.ForeignKey(InterventionType, null=True, blank=True)
    name_specified = models.CharField(max_length=250, null=True, blank=True)
    hts_result = models.ForeignKey(HTSResult, null=True, blank=True)
    pregnancy_test_result = models.ForeignKey(PregnancyTestResult, null=True, blank=True)
    client_ccc_number = models.CharField(max_length=11, blank=True, null=True)
    date_linked_to_ccc = models.DateField(blank=True, null=True)
    no_of_sessions_attended = models.IntegerField(null=True, blank=True)
    comment = models.TextField(max_length=256, null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, related_name='created_by')
    date_changed = models.DateTimeField(null=True, blank=True)
    changed_by = models.ForeignKey(User, null=True, blank=True, related_name='changed_by')
    implementing_partner = models.ForeignKey(ImplementingPartner, null=True, blank=True,
                                             related_name='implementing_partner')

    def get_name_specified(self):
        return self.name_specified if self.name_specified else ''

    def save(self, user_id=None, action=None, *args, **kwargs):  # pass audit to args as the first object
        super(Intervention, self).save(*args, **kwargs)
        audit = Audit()
        audit.user_id = user_id
        audit.table = "DreamsApp_intervention"
        audit.row_id = self.pk
        audit.action = action
        audit.search_text = None
        audit.save()

    def __str__(self):
        return '{} {}'.format(self.intervention_type, self.created_by)

    class Meta(object):
        verbose_name = 'Intervention'
        verbose_name_plural = 'Interventions'


class Audit(models.Model):
    timestamp = models.DateTimeField(auto_now=True, blank=False, null=False)
    user_id = models.IntegerField(blank=False, null=False)
    table = models.CharField(max_length=200, default='', blank=False, null=False)
    row_id = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=100, blank=False, null=False)
    search_text = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '{} by user id {} at {}'.format(self.action, self.user_id, self.timestamp)

    class Meta(object):
        verbose_name = 'Audit'
        verbose_name_plural = 'Audit log'


class GrievanceReporterCategory(models.Model):
    """ Model containing the Category of Grievance Reporter """
    code = models.IntegerField(name='code', verbose_name='Code')
    name = models.CharField(max_length=50, verbose_name='Name')
    requires_dreams_id = models.BooleanField(default=False, verbose_name='Requires DREAMS ID')
    requires_relationship = models.BooleanField(default=False, verbose_name='Requires Relationship Specification')
    is_other_specified = models.BooleanField(default=False, verbose_name='Other Specify')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Grievance Reporter Category'
        verbose_name_plural = 'Grievance Reporter Categories'


class GrievanceNature(models.Model):
    """ Model containing the nature of the Grievance reported """
    code = models.IntegerField(name='code', verbose_name='Code')
    name = models.CharField(max_length=50, verbose_name='Name')
    is_other_specify = models.BooleanField(default=False, verbose_name='Other Specify')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Nature of Grievance'
        verbose_name_plural = 'Grievance Nature List'


class GrievanceStatus(models.Model):
    """ Model containing Grievance Status"""
    code = models.IntegerField(name='code', verbose_name='Code')
    name = models.CharField(max_length=50, verbose_name='Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Grievance Status'
        verbose_name_plural = 'Grievance Status List'


class Grievance(models.Model):
    """ Model for Grievance Reporting """
    date = models.DateField(null=True, blank=True, default=datetime.now, verbose_name='Date Reported')
    implementing_partner = models.ForeignKey(ImplementingPartner, null=False, blank=False,
                                             verbose_name='Implementing Partner')
    county = models.ForeignKey(County, null=False, blank=False, related_name='county', verbose_name='County')
    ward = models.ForeignKey(Ward, null=False, blank=False, related_name='ward', verbose_name='Ward')
    reporter_name = models.CharField(verbose_name='Reporter Name', max_length=250, null=False, blank=False)
    reporter_category = models.ForeignKey(GrievanceReporterCategory, null=False, blank=False, related_name='reporter_category',
                                          verbose_name='Reporter Category')
    dreams_id = models.CharField(verbose_name='DREAMS ID', max_length=150, null=True, blank=True)
    relationship = models.CharField(verbose_name='Relationship', max_length=50, null=True, blank=True)
    other_specify = models.CharField(verbose_name='Specify', max_length=150, null=True, blank=True)
    reporter_phone = models.CharField(verbose_name='Complainant’s Telephone No', max_length=13, null=True, blank=True)
    received_by = models.CharField(verbose_name='Name of DREAMS staff receiving the grievance', max_length=250,
                                   null=False, blank=False)
    receiver_designation = models.CharField(verbose_name='Designation', max_length=50, null=True, blank=True)
    grievance_nature = models.ForeignKey(GrievanceNature, null=False, blank=False, verbose_name='Nature of Grievance',
                                         related_name='grievance_nature')
    other_grievance_specify = models.CharField(verbose_name='Specify Grievance', max_length=250, null=True, blank=True)
    is_first_time_complaint = models.BooleanField(default=False, verbose_name='Is a 1st Time Complaint')
    person_responsible = models.CharField(verbose_name='Person Responsible', max_length=250,
                                   null=True, blank=True)
    resolution = models.TextField(verbose_name='Resolution', null=True, blank=True)
    resolution_date = models.DateField(null=True, blank=True, default=datetime.now, verbose_name='Date of resolution')
    complainant_feedback_date = models.DateField(null=True, blank=True, verbose_name='Date of Feedback to Complainant')
    status = models.ForeignKey(GrievanceStatus, null=True, blank=True, default=1, verbose_name='Status')
    closed_by = models.CharField(verbose_name='Closed by', max_length=250,
                                 null=True, blank=True)
    closure_date = models.DateField(null=True, blank=True, default=datetime.now, verbose_name='Date Closed')
    created_by = models.ForeignKey(User, null=True, blank=True, verbose_name='Created By')
    created_at = models.DateTimeField(null=False, blank=True, default=datetime.now, verbose_name='Created at')
    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='modified_by', verbose_name='Modified By')
    modified_at = models.DateTimeField(null=True, blank=True, default=datetime.now, verbose_name='Modified at')

    def __str__(self):
        return '{}'.format(self.grievance_nature)

    class Meta(object):
        verbose_name = 'Grievance'
        verbose_name_plural = 'Grievances'
        ordering = ['-date']


class PaymentMode(models.Model):
    """ Model containing Payment Modes """
    code = models.IntegerField(name='code', verbose_name='Code')
    name = models.CharField(max_length=50, verbose_name='Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta(object):
        verbose_name = 'Payment Mode'
        verbose_name_plural = 'Payment Modes'


class ClientCashTransferDetails(models.Model):
    """ Client Cash Transfer Details """
    client = models.OneToOneField(Client, null=False, blank=False, verbose_name='Dreams Beneficiary\(AGYW\)')
    is_client_recepient = models.BooleanField(default=False, verbose_name='Is AGYW the Recepient?')
    recipient_name = models.CharField(verbose_name='Reporter Name', max_length=250, null=True, blank=True)
    recipient_relationship_with_client = models.CharField(verbose_name='Relationship with AGYW', max_length=150,
                                                          null=True, blank=True)
    payment_mode = models.ForeignKey(PaymentMode, null=False, blank=False, verbose_name='Prefered Mode of '
                                                                                        'receiving Cash')
    mobile_service_provider_name = models.CharField(verbose_name='Name of Mobile Service Provider', max_length=250, null=True, blank=True)
    recipient_phone_number = models.CharField(verbose_name='Phone No', max_length=13, null=True, blank=True)
    bank_name = models.CharField(verbose_name='Bank', max_length=250, null=True, blank=True)
    bank_branch_name = models.CharField(verbose_name='Branch', max_length=250, null=True, blank=True)
    bank_account_name = models.CharField(verbose_name='Account name', max_length=250, null=True, blank=True)
    bank_account_number = models.CharField(verbose_name='Account number', max_length=250, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.recipient_name, self.recipient_phone_number)

    class Meta(object):
        verbose_name = 'Cash Transfer Detail'
        verbose_name_plural = 'Cash Transfer Details'




