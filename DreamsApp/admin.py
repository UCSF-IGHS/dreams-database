from django.contrib import admin

from models import *
# Register your models here.

class WomanAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'date_of_birth')
    list_per_page = 15
    search_fields = ('first_name', 'last_name', 'date_of_birth')

admin.site.register(Woman, WomanAdmin)

class InterventionCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)
    search_fields = ('name',)

admin.site.register(InterventionCategory, InterventionCategoryAdmin)

class InterventionTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('name',)

admin.site.register(InterventionType, InterventionTypeAdmin)

admin.site.register(Intervention)

admin.site.register(HIVTestResult)
