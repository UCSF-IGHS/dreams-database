
from django.contrib import admin
from django.contrib.auth.models import Permission
from DreamsApp.forms import *
from DreamsApp.models import *
# Register your models here.
from django.forms import CheckboxSelectMultiple
from django.core.urlresolvers import reverse


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'content_type')
    search_fields = ('name', 'codename', 'content_type')

admin.site.register(Permission, PermissionAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'date_of_birth')
    list_per_page = 15
    search_fields = ('first_name', 'last_name', 'date_of_birth')

admin.site.register(Client, ClientAdmin)


class InterventionCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)
    search_fields = ('name',)

admin.site.register(InterventionCategory, InterventionCategoryAdmin)


class InterventionTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_age_restricted', 'min_age', 'max_age', 'is_given_once', 'is_specified')
    search_fields = ('name',)

admin.site.register(InterventionType, InterventionTypeAdmin)
admin.site.register(HTSResult)
admin.site.register(PregnancyTestResult)
admin.site.register(Intervention)
admin.site.register(MaritalStatus)
admin.site.register(County)
admin.site.register(SubCounty)
admin.site.register(Ward)
admin.site.register(VerificationDocument)
admin.site.register(ImplementingPartner)
admin.site.register(DreamsProgramme)
admin.site.register(Drug)
admin.site.register(GBVHelpProvider)
admin.site.register(ReasonNotTestedForHIV)
admin.site.register(FamilyPlanningMethod)
admin.site.register(ReasonNotUsingFamilyPlanning)
admin.site.register(AgeOfSexualPartner)
admin.site.register(FrequencyResponse)
admin.site.register(ReasonNotInHIVCare)
admin.site.register(ReasonNotInSchool)
admin.site.register(HivTestResultResponse)
admin.site.register(BankingPlace)
admin.site.register(SourceOfIncome)
admin.site.register(LifeWish)
admin.site.register(EducationSupporter)
admin.site.register(SchoolLevel)
admin.site.register(SchoolType)
admin.site.register(DisabilityType)
admin.site.register(DrinkingWater)
admin.site.register(FloorMaterial)
admin.site.register(WallMaterial)
admin.site.register(RoofingMaterial)
admin.site.register(HouseholdHead)
admin.site.register(PeriodResponse)
admin.site.register(CategoricalResponse)
admin.site.register(AgeBracket)
admin.site.register(InterventionPackage)
admin.site.register(ClientIndividualAndHouseholdData) # verified
admin.site.register(ClientEducationAndEmploymentData)
admin.site.register(ClientHIVTestingData)
admin.site.register(ClientSexualActivityData)
admin.site.register(ClientReproductiveHealthData)
admin.site.register(ClientGenderBasedViolenceData)
admin.site.register(ClientDrugUseData)
admin.site.register(ClientParticipationInDreams)
admin.site.register(ConfigurableParameter)


class AuditAdmin(admin.ModelAdmin):
    model = Audit
    list_display = ('user_id', 'table', 'row_id', 'action', 'search_text', 'timestamp')
    search_fields = ('user_id', 'table', 'action')

admin.site.register(Audit, AuditAdmin)


class ImplementingPartnerUserAdmin(admin.ModelAdmin):
    model = ImplementingPartnerUser
    list_display = ('get_username', 'implementing_partner')
    list_per_page = 15

    def get_username(self, object):
        return object.user

    get_username.short_description = 'Username'


admin.site.register(ImplementingPartnerUser, ImplementingPartnerUserAdmin)


class GrievanceReporterCategoryAdmin(admin.ModelAdmin):
    model = GrievanceReporterCategory
    list_display = ('code', 'name', 'requires_dreams_id', 'requires_relationship', 'is_other_specified')
    list_per_page = 25

admin.site.register(GrievanceReporterCategory, GrievanceReporterCategoryAdmin)


class GrievanceNatureAdmin(admin.ModelAdmin):
    model = GrievanceNature
    list_display = ('code', 'name', 'is_other_specify')
    list_per_page = 25

admin.site.register(GrievanceNature, GrievanceNatureAdmin)


class GrievanceStatusAdmin(admin.ModelAdmin):
    model = GrievanceStatus
    list_display = ('code', 'name')
    list_per_page = 25

admin.site.register(GrievanceStatus, GrievanceStatusAdmin)


class GrievanceAdmin(admin.ModelAdmin):
    model = Grievance
    list_display = ('date', 'implementing_partner', 'county', 'ward', 'reporter_name', 'reporter_category', 'grievance_nature', 'other_grievance_specify', 'is_first_time_complaint', 'person_responsible', 'resolution', 'resolution_date', 'complainant_feedback_date', 'status')
    search_fields = (
    'date', 'implementing_partner', 'county', 'ward', 'reporter_name', 'reporter_category', 'grievance_nature',
    'other_grievance_specify', 'is_first_time_complaint', 'person_responsible', 'resolution', 'resolution_date',
    'complainant_feedback_date', 'status')
    list_per_page = 30

admin.site.register(Grievance, GrievanceAdmin)


class ClientCashTransferDetailsAdmin(admin.ModelAdmin):
    model = ClientCashTransferDetails
    list_display = ('client', 'recipient_name', 'recipient_relationship_with_client', 'payment_mode',
                    'mobile_service_provider_name', 'recipient_phone_number', 'bank_name', 'bank_account_number')
    list_per_page = 30

admin.site.register(ClientCashTransferDetails, ClientCashTransferDetailsAdmin)


class PaymentModeAdmin(admin.ModelAdmin):
    model = PaymentMode
    list_display = ('code', 'name')
    list_per_page = 25

admin.site.register(PaymentMode, PaymentModeAdmin)


class ServicePackageInterventionTypeAlternativeInline(admin.TabularInline):
    model = ServicePackage.intervention_type_alternatives.through
    extra = 0


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    model = ServicePackage
    inlines = [ServicePackageInterventionTypeAlternativeInline, ]
    list_display = ('name', 'description', 'lower_age_limit', 'upper_age_limit', 'age_group', 'date_created',
                    'created_by', 'date_changed', 'changed_by')
    fieldsets = (
        ('Service package details', {
            'fields': ('name', 'description', 'lower_age_limit', 'upper_age_limit',)
        }),
        ('Auto-generated info', {
            'fields': ('age_group', 'created_by', 'date_changed', 'changed_by'),
            'classes': ['collapse in', ]
        }),
    )
    list_per_page = 25
    list_filter = ('name', 'description', 'lower_age_limit', 'upper_age_limit', 'age_group')
    empty_value_display = '-'
    exclude = ('intervention_type_alternatives',)
    filter_horizontal = ['intervention_type_alternatives', ]

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('age_group', 'date_created', 'created_by', 'date_changed', 'changed_by')

    def save_model(self, request, obj, form, change):
        if not obj.id is not None:
            obj.created_by = request.user
        else:
            obj.changed_by = request.user
        obj.save()


@admin.register(InterventionTypeAlternative)
class ServicePackageInterventionTypeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    empty_value_display = '-'
    list_display = ('description', 'package_option_category', 'intervention_type_alternatives_text', )
    list_per_page = 25
    list_filter = ('intervention_type_alternatives_text', 'package_option_category')
    fieldsets = (
        ('', {
            'fields': ('name', 'description', 'package_option_category', 'intervention_type_alternatives', )
        }),
        ('Auto-generated info', {
            'fields': ('intervention_type_alternatives_text', ),
            'classes': ['collapse in', ]
        })
    )

    def save_model(self, request, obj, form, change):
        model_form = self.get_form(request, obj)
        if request.method == 'POST':
            form = model_form(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            intervention_type_alternatives_text = u''
            for iv_type_alternatives in form.cleaned_data['intervention_type_alternatives'].all().order_by('name'):
                if intervention_type_alternatives_text.encode('utf8') == '':
                    intervention_type_alternatives_text = '{}'.format(iv_type_alternatives.name)
                else:
                    intervention_type_alternatives_text = u'{}, {}'.format(intervention_type_alternatives_text,
                                                                           iv_type_alternatives.name)
            obj.intervention_type_alternatives_text = intervention_type_alternatives_text
            super(ServicePackageInterventionTypeAdmin, self).save_model(request, obj, form, change)
            return obj
        else:
            raise Exception("An error occurred while processing your request. "
                            "Please contact system administrator for help")

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('intervention_type_alternatives_text', )


@admin.register(InterventionTypePackage)
class InterventionTypePackageAdmin(admin.ModelAdmin):
    list_display = ('intervention_type', 'intervention_package', 'lower_age_limit', 'upper_age_limit',)