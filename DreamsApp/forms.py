# coding=utf-8
from django.forms import ModelForm, forms
from models import *

# DreamsApp imports
from DreamsApp.models import Grievance, ImplementingPartner, ClientCashTransferDetails, Client, ClientIndividualAndHouseholdData, \
    ClientEducationAndEmploymentData, ClientSexualActivityData, ClientReproductiveHealthData, ClientGenderBasedViolenceData, ClientDrugUseData, \
    ClientParticipationInDreams, ClientHIVTestingData


class GrievanceModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(GrievanceModelForm, self).__init__(*args, **kwargs)

    class Meta(object):
            model = Grievance
            fields = '__all__'
            exclude = ['created_by', 'created_at', 'modified_by', 'modified_at']


class ClientCashTransferDetailsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        current_AGYW = kwargs.pop('current_AGYW', None)
        super(ClientCashTransferDetailsForm, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = \
            Client.objects.filter(id=current_AGYW.id) \
                if current_AGYW is not None \
                else Client.objects.all()

    class Meta(object):
        model = ClientCashTransferDetails
        fields = '__all__'


class DemographicsForm(ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['enrolled_by', 'odk_enrollment_uuid', 'date_created', 'date_changed', 'is_date_of_birth_estimated', 'age_at_enrollment']


class IndividualAndHouseholdForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(IndividualAndHouseholdForm, self).__init__(*args, **kwargs)
        self.fields['is_father_alive'].queryset = CategoricalResponse.objects.exclude(pk=4)
        self.fields['is_mother_alive'].queryset = CategoricalResponse.objects.exclude(pk=4)
        self.fields['ever_missed_full_day_food_in_4wks'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['no_of_days_missed_food_in_4wks'].queryset = FrequencyResponse.objects.filter(pk__in=[1, 2, 3])
        self.fields['has_disability'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['ever_enrolled_in_ct_program'].queryset = CategoricalResponse.objects.exclude(pk=4)
        self.fields['currently_in_ct_program'].queryset = CategoricalResponse.objects.exclude(pk=4)

    class Meta:
        model = ClientIndividualAndHouseholdData
        fields = '__all__'
        exclude = ['date_changed', 'date_created']



class EducationAndEmploymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EducationAndEmploymentForm, self).__init__(*args, **kwargs)
        self.fields['currently_in_school'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['last_time_in_school'].queryset = PeriodResponse.objects.filter(pk__in=[1, 2, 3, 4, 5])
        self.fields['has_savings'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])

    class Meta:
        model = ClientEducationAndEmploymentData
        fields = '__all__'
        exclude = ['date_created', 'date_changed']



class HivTestForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(HivTestForm, self).__init__(*args, **kwargs)
        self.fields['ever_tested_for_hiv'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['period_last_tested'].queryset = PeriodResponse.objects.filter(pk__in=[6, 7, 8, 9])
        self.fields['enrolled_in_hiv_care'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['knowledge_of_hiv_test_centres'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])

    class Meta:
        model = ClientHIVTestingData
        fields = '__all__'
        exclude = ['date_created', 'date_changed']



class SexualityForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SexualityForm, self).__init__(*args, **kwargs)
        self.fields['ever_had_sex'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['has_sexual_partner'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])

        self.fields['last_partner_circumcised'].queryset = CategoricalResponse.objects.exclude(pk=4)
        self.fields['second_last_partner_circumcised'].queryset = CategoricalResponse.objects.exclude(pk=4)
        self.fields['third_last_partner_circumcised'].queryset = CategoricalResponse.objects.exclude(pk=4)

        self.fields['know_last_partner_hiv_status'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['know_second_last_partner_hiv_status'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['know_third_last_partner_hiv_status'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])

        self.fields['used_condom_with_last_partner'].queryset = FrequencyResponse.objects.filter(pk__in=[4, 5, 6])
        self.fields['used_condom_with_second_last_partner'].queryset = FrequencyResponse.objects.filter(pk__in=[4, 5, 6])
        self.fields['used_condom_with_third_last_partner'].queryset = FrequencyResponse.objects.filter(pk__in=[4, 5, 6])
        self.fields['received_money_gift_for_sex'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])

    class Meta:
        model = ClientSexualActivityData
        fields = '__all__'
        exclude = ['date_created', 'date_changed']


class ReproductiveHealthForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReproductiveHealthForm, self).__init__(*args, **kwargs)
        self.fields['has_biological_children'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['currently_pregnant'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2, 3])
        self.fields['current_anc_enrollment'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['fp_methods_awareness'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['currently_use_modern_fp'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])


    class Meta:
        model = ClientReproductiveHealthData
        fields = '__all__'
        exclude = ['date_created', 'date_changed']



class GBVForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(GBVForm, self).__init__(*args, **kwargs)
        self.fields['humiliated_ever'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['humiliated_last_3months'].queryset = FrequencyResponse.objects.filter(pk__in=[7, 5, 8])

        self.fields['threats_to_hurt_ever'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['threats_to_hurt_last_3months'].queryset = FrequencyResponse.objects.filter(pk__in=[7, 5, 8])

        self.fields['insulted_ever'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['insulted_last_3months'].queryset = FrequencyResponse.objects.filter(pk__in=[7, 5, 8])

        self.fields['economic_threat_ever'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['economic_threat_last_3months'].queryset = FrequencyResponse.objects.filter(pk__in=[7, 5, 8])

        self.fields['physical_violence_ever'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['physical_violence_last_3months'].queryset = FrequencyResponse.objects.filter(pk__in=[7, 5, 8])

        self.fields['physically_forced_sex_ever'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['physically_forced_sex_last_3months'].queryset = FrequencyResponse.objects.filter(pk__in=[7, 5, 8])

        self.fields['physically_forced_other_sex_acts_ever'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['physically_forced_other_sex_acts_last_3months'].queryset = FrequencyResponse.objects.filter(pk__in=[7, 5, 8])

        self.fields['threatened_for_sexual_acts_ever'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['threatened_for_sexual_acts_last_3months'].queryset = FrequencyResponse.objects.filter(pk__in=[7, 5, 8])

        self.fields['seek_help_after_gbv'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['knowledge_of_gbv_help_centres'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])

    class Meta:
        model = ClientGenderBasedViolenceData
        fields = '__all__'
        exclude = ['date_created', 'date_changed']



class DrugUseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DrugUseForm, self).__init__(*args, **kwargs)
        self.fields['used_alcohol_last_12months'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['frequency_of_alcohol_last_12months'].queryset = FrequencyResponse.objects.filter(pk__in=[9, 10, 11, 12, 13, 14, 15, 16])
        self.fields['drug_abuse_last_12months'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])
        self.fields['produced_alcohol_last_12months'].queryset = CategoricalResponse.objects.filter(pk__in=[1, 2])

    class Meta:
        model = ClientDrugUseData
        fields = '__all__'
        exclude = ['date_created', 'date_changed']



class DreamsProgramParticipationForm(ModelForm):

    class Meta:
        model = ClientParticipationInDreams
        fields = '__all__'
        exclude = ['date_created', 'date_changed']

