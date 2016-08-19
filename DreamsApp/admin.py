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


class AuditAdmin(admin.ModelAdmin):
    model = Audit
    list_display = ('user_id', 'table', 'row_id', 'action', 'search_text', 'timestamp')
    search_fields = ('user_id', 'table', 'action')

admin.site.register(Audit, AuditAdmin)


class InitAppAdmin(admin.ModelAdmin):
    model = InitApp

admin.site.register(InitApp, InitAppAdmin)


class ImplementingPartnerUserAdmin(admin.ModelAdmin):
    model = ImplementingPartnerUser
    list_display = ('get_username', 'implementing_partner')
    list_per_page = 15

    def get_username(self, object):
        return object.user

    get_username.short_description = 'Username'


admin.site.register(ImplementingPartnerUser, ImplementingPartnerUserAdmin)
