from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class MaritalStatus(models.Model):
    code = models.CharField(verbose_name='Marital Status Code', max_length=10, null=False, blank=False)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Marital Status'
        verbose_name_plural = 'Marital Status'


class County(models.Model):
    code = models.CharField(verbose_name='County Code', max_length=10, default='', null=False, blank=False)
    name = models.CharField(verbose_name='County', max_length=100, default='', null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'County'
        verbose_name_plural = 'Counties'


class SubCounty(models.Model):
    county = models.ForeignKey(County, null=True, blank=True)
    code = models.CharField(verbose_name='Sub County Code', max_length=100, default='', null=False, blank=False)
    name = models.CharField(verbose_name='Sub County', max_length=100, default='', null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Sub County'
        verbose_name_plural = 'Sub Counties'


class Ward(models.Model):
    sub_county = models.ForeignKey(SubCounty, null=True, blank=True)
    code = models.CharField(verbose_name='Ward Code', max_length=100, default='', null=False, blank=False)
    name = models.CharField(verbose_name='Ward', max_length=100, default='', null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Ward'
        verbose_name_plural = 'Wards'


class VerificationDocument(models.Model):
    code = models.IntegerField(name='code', verbose_name='Verification Document Code')
    name = models.CharField(max_length=150, verbose_name='Verification Document Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Verification Document'
        verbose_name_plural = 'Verification Documents'


class ImplementingPartner(models.Model):
    code = models.IntegerField(name='code', verbose_name='Implementing Partner Code')
    name = models.CharField(max_length=150, verbose_name='Implementing Partner Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Implementing Partner'
        verbose_name_plural = 'Implementing Partners'


class ImplementingPartnerUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    implementing_partner = models.ForeignKey(ImplementingPartner, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    class Meta:
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
    guardian_phone_number = models.CharField(verbose_name='Phone Number(Care giver / Guardian)', max_length=13, null=True)
    guardian_national_id = models.CharField(verbose_name='National ID (Care giver / Guardian)', max_length=10, null=True)

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

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class InterventionCategory(models.Model):
    code = models.IntegerField(verbose_name='Intervention Category Code', default=0)
    name = models.CharField(max_length=30)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
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

    class Meta:
        verbose_name = 'Intervention Type'
        verbose_name_plural = 'Intervention Types'


class HTSResult(models.Model):
    code = models.IntegerField(name='code', verbose_name='HTS Result Code')
    name = models.CharField(max_length=20, verbose_name='HTS Result Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'HTS Result'
        verbose_name_plural = 'HTS Results'


class PregnancyTestResult(models.Model):
    code = models.IntegerField(name='code', verbose_name='Pregnancy Result Code')
    name = models.CharField(max_length=20, verbose_name='Pregnancy Result Name')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
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

    def save(self,user_id=None, action=None, *args, **kwargs): # pass audit to args as the first object
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

    class Meta:
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

    class Meta:
        verbose_name = 'Audit'
        verbose_name_plural = 'Audit log'


class InitApp(models.Model):
    timestamp = models.DateTimeField(auto_now=True, blank=False, null=False)
    inited = models.BooleanField(default=False, blank=False, null=False)


""" Models for Responses to questions on enrollment form"""


class CategoricalResponse(models.Model):
    """ Include the Yes, No, Unknown responses to questions"""
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name='Response Name')
    code = models.IntegerField(verbose_name='Response Code')

    def __str__(self):
        return "{} {} ".format(self.name, self.code)

    class Meta:
        verbose_name = 'Yes|No Response'
        verbose_name_plural = 'Yes|No Responses'


class PeriodResponse(models.Model):
    """Include answers to the how frequent event occurs e.g last 3 months, last 6 months etc"""
    name = models.CharField(max_length=50, blank=False, null=False,  verbose_name='Response Name')
    code = models.IntegerField(verbose_name='Response Code')

    def __str__(self):
        return "{} {} ".format(self.name, self.code)

    class Meta:
        verbose_name = 'Duration Response'
        verbose_name_plural = 'Duration Responses'


class HouseholdHead(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    code = models.IntegerField(verbose_name='Household Head Code')

    def __str__(self):
        return "{} {} ".format(self.name, self.code)

    class Meta:
        verbose_name = 'Head of Household Category'
        verbose_name_plural = 'Head of Household Categories'


class RoofingMaterial(models.Model):
    name = models.CharField(verbose_name='Material Name', max_length=50, blank=False, null=False)
    code = models.IntegerField(verbose_name='Material Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Main Roofing Materials'
        verbose_name = 'Main Roofing Material'


class WallMaterial(models.Model):
    name = models.CharField(verbose_name='Material Name', max_length=50, blank=False, null=False)
    code = models.IntegerField(verbose_name='Material Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Main Wall Materials'
        verbose_name = 'Main Wall Material'


class FloorMaterial(models.Model):
    name = models.CharField(verbose_name='Material Name', max_length=50, blank=False, null=False)
    code = models.IntegerField(verbose_name='Material Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Main Floor Materials'
        verbose_name = 'Main Floor Material'


class DrinkingWater(models.Model):
    """Documents main source of household's drinking water"""
    name = models.CharField(verbose_name='Water Source', max_length=50, blank=False, null=False)
    code = models.IntegerField(verbose_name='Source Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Drinking water Sources'
        verbose_name = 'Drinking Water Source'


class DisabilityType(models.Model):
    """Documents type of disability i.e hearing etc"""
    name = models.CharField(verbose_name='Name of Disability', max_length=50, blank=False, null=False)
    code = models.IntegerField(verbose_name='Disability Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Disability Types'
        verbose_name = 'Disability Type'


class SchoolType(models.Model):
    """A model for school type i.e formal, informal"""
    name = models.CharField(max_length=50, blank=False, null=False)
    code = models.IntegerField(verbose_name='Type Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'School Types'
        verbose_name = 'School Type'


class EducationLevel(models.Model):
    """A model for level of educaton i.e Primary, Secondary etc"""
    name = models.CharField(verbose_name='Education Level Name', max_length=50, blank=False, null=False)
    code = models.IntegerField(verbose_name='Education Level Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Levels of Education'
        verbose_name = 'Level of Education'


class EducationSupport(models.Model):
    """A model for source of education support i.e Gov bursary, NGO etc"""
    name = models.CharField(max_length=50, blank=False, null=False, verbose_name='Name')
    code = models.IntegerField(blank=False)

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Sources of Education Support'
        verbose_name = 'Source of Education Support'


class ReasonNotInSchool(models.Model):
    """Reason why one is not in school"""
    name = models.CharField(verbose_name='Reason', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Reason Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Reasons not in School'
        verbose_name = 'Reason not in School'


class LifeWish(models.Model):
    """One's life wish"""
    name = models.CharField(verbose_name='Wish', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Wish Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Life Wishes'
        verbose_name = 'Life Wish'


class SourceOfIncome(models.Model):
    """Main source of income"""
    name = models.CharField(verbose_name='Source', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Sources of Income'
        verbose_name = 'Source of Income'


class BankingPlace(models.Model):
    """A place where savings are kept e.g Bank etc"""
    name = models.CharField(verbose_name='Banking Place', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Banking Places'
        verbose_name = 'Banking Place'


class HivTestResultResponse(models.Model):
    """Record of last HIV test result and includes Don't know and Declined"""
    name = models.CharField(verbose_name='Response', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'HIV Test Responses'
        verbose_name = 'HIV Test Response'


class ReasonNotInHIVCare(models.Model):
    """Reason one doesn't seek HIV care"""
    name = models.CharField(verbose_name='Response', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Reasons not in HIV Care'
        verbose_name = 'Reason not in HIV Care'


class ReasonNotTestedForHIV(models.Model):
    """Reason one has never been tested for HIV"""
    name = models.CharField(verbose_name='Response', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Reasons not tested for HIV '
        verbose_name = 'Reason not tested for HIV'


class AgeOfSexualPartner(models.Model):
    """Age of sexual partner"""
    name = models.CharField(verbose_name='Age Category', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Age of Sexual Partner '


class FrequencyResponse(models.Model):
    """Captures frequency of an event i.e always, sometimes, never etc """
    name = models.CharField(verbose_name='Frequency', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Frequency Responses'
        verbose_name = 'Frequency Response'


class FamilyPlanningMethod(models.Model):
    """model for Family Planning Method i.e Pills, Injectables etc """
    name = models.CharField(verbose_name='Method', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Family Planning methods'
        verbose_name = 'Family Planning method'


class ReasonNotUsingFamilyPlanning(models.Model):
    """Reason why one doesn't use FP  """
    name = models.CharField(verbose_name='Reason', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Reasons not using Family Planning'
        verbose_name = 'Reason not using Family Planning'


class GBVSupport(models.Model):
    """Source of GBV support """
    name = models.CharField(verbose_name='Source of Support', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Sources of GBV Support'
        verbose_name = 'Source of GBV Support'


class DrugAbuse(models.Model):
    """Drug abuse/addiction i.e miraa, bhang etc """
    name = models.CharField(verbose_name='Drug Abuse/Addiction', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Drug Abuse'


class DreamsProgramme(models.Model):
    """Drug abuse/addiction i.e miraa, bhang etc """
    name = models.CharField(verbose_name='Name of Programme', max_length=50, blank=False, null=False)
    code = models.IntegerField(blank=False, verbose_name='Code')

    def __str__(self):
        return '{} {}'.format(self.name, self.code)

    class Meta:
        verbose_name_plural = 'Dreams Programmes'
        verbose_name = 'Dreams Programme'


""" Models for the different modules in enrollment form """


class IndividualAndHouseholdInformation(models.Model):
    """ Holds individual and household information about Dreams client"""
    client = models.ForeignKey(Client)
    household_head = models.ForeignKey(HouseholdHead)
    household_head_other = models.CharField(max_length=50, blank=True, null=True)
    age_of_household_head = models.IntegerField(default=0, blank=True)
    hh_father_alive = models.IntegerField(verbose_name='Father alive?')
    hh_mother_alive = models.IntegerField(verbose_name='Mother alive?')
    hh_parent_chronical_illness = models.IntegerField(verbose_name='Is any of your parent/guardian chronically ill?')
    hh_main_floor_material = models.ForeignKey(FloorMaterial, verbose_name='Main floor material', null=True)
    hh_main_floor_material_other = models.CharField(max_length=50, verbose_name='Main floor material: other', blank=True, null=True)
    hh_main_roof_material = models.ForeignKey(RoofingMaterial, verbose_name='Main roof material', null=True)
    hh_main_roof_material_other = models.CharField(max_length=50, verbose_name='Main roof material: other', blank=True, null=True)
    hh_main_wall_material = models.ForeignKey(RoofingMaterial, verbose_name='Main wall material', null=True)
    hh_main_wall_material_other = models.CharField(max_length=50, verbose_name='Main wall material: other', blank=True,
                                                   null=True)
    hh_drinking_water = models.ForeignKey(DrinkingWater, verbose_name='Main source of drinking water', null=True)
    hh_drinking_water_other = models.CharField(max_length=50, verbose_name='Main source of drinking water: other', blank=True,
                                                   null=True)
    hh_missed_food_within_4wks = models.ForeignKey(CategoricalResponse, null=True)
    hh_days_missed_food_within_4wks = models.ForeignKey(FrequencyResponse, blank=True)
    hh_has_disability = models.ForeignKey(CategoricalResponse, verbose_name='Disabled?', blank=True, null=True)
    hh_disability_type = models.ForeignKey(DisabilityType, null=True, verbose_name='Disability Type')
    hh_disability_type_other = models.CharField(verbose_name='Other disability type', blank=True, null=True)
    hh_no_of_people_in_household = models.IntegerField(verbose_name='No of people living in your house')
    hh_no_of_females = models.IntegerField(verbose_name='No of females')
    hh_no_of_males = models.IntegerField(verbose_name='No of Males')
    hh_no_adults = models.IntegerField(verbose_name='No of adults')
    hh_no_children = models.IntegerField(verbose_name='No of children')
    hh_ever_enrolled_in_ct = models.ForeignKey(CategoricalResponse, verbose_name='Ever enrolled in Cash Transfer?')
    hh_currently_in_ct = models.ForeignKey(CategoricalResponse, verbose_name="Currently enrolled in Cash Transfer?")
    hh_current_ct_prog_enrolled = models.CharField(verbose_name='Cash Transfer Programme currently enrolled in')


class ClientEducationAndEmployment(models.Model):
    """ Holds education and employment information about Dreams client"""
    client = models.ForeignKey(Client)
    edu_currently_schooling = models.ForeignKey(CategoricalResponse, verbose_name='Currently schooling')
    edu_name_of_school = models.CharField(verbose_name='Name of school', blank=True, null=True)
    edu_type_of_school = models.ForeignKey(SchoolType, verbose_name='Type of school', blank=True, null=True)
    edu_current_edu_level = models.ForeignKey(EducationLevel, verbose_name='Current school level', null=True, blank=True)
    edu_current_edu_level_class = models.CharField(verbose_name='Class', max_length=10, blank=True, null=True)
    edu_current_edu_level_other = models.CharField(verbose_name='Other Education Level', max_length=20, blank=True, null=True)
    edu_current_education_support = models.ForeignKey(EducationSupport, verbose_name='Support towards current education')
    edu_current_education_support_other = models.CharField(max_length=25, verbose_name='Support towards current education: other')
    edu_reason_not_in_school = models.ForeignKey(ReasonNotInSchool, verbose_name='Reason for not going to school')
    edu_reason_not_in_school_other = models.CharField(verbose_name='Reason for not going to school: other')
    edu_last_time_in_school = models.ForeignKey(PeriodResponse, verbose_name='Last time in school')
    edu_drop_out_school_level = models.ForeignKey(EducationLevel, 'In which class/form did you stop schooling?')
    edu_drop_out_class = models.CharField(max_length=15, verbose_name='Drop out class')
    edu_life_wish = models.ForeignKey(LifeWish, verbose_name='Wish in life', blank=True, null=True)
    edu_life_wish_other = models.CharField(verbose_name='Wish in life: other', max_length=50, blank=True, null=True)
    edu_current_income_source = models.ForeignKey(SourceOfIncome, verbose_name='Current source of income')
    edu_current_income_source_other = models.CharField(verbose_name='Source of income: other', max_length=30)
    edu_has_savings = models.ForeignKey(CategoricalResponse, verbose_name='Do you have savings?')
    edu_banking_place = models.ForeignKey(BankingPlace, verbose_name='Where do you keep your savings?', blank=True, null=True)
    edu_banking_place_other = models.CharField(max_length=20, verbose_name='Other place for savings')


class ClientHIVTesting(models.Model):
    """ Holds HIV testing information about a client"""
    pass


class ClientSexualActivity(models.Model):
    """ Holds Sexual activity information about a client"""
    pass


class ClientReproductivity(models.Model):
    """ Holds information about client's reproductivity """
    pass


class ClientGBV(models.Model):
    """Holds Gender Based Violence information about a client"""
    pass


class ClientDrugUse(models.Model):
    """ Holds Drug use information about client"""
    pass


class ClientParticipationInHIVProgramme(models.Model):
    """ Holds information of client's participation in HIV programmes"""
    pass



