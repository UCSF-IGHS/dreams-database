# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import Permission

from models import *
# Register your models here.

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