# coding=utf-8
"""Dreams URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, handler400, handler403, handler404, handler500
from django.contrib import admin
from DreamsApp import views

# handler400 = 'DreamsApp.views.bad_request'
handler403 = 'DreamsApp.views.permission_denied'
handler404 = 'DreamsApp.views.page_not_found'
# handler500 = 'DreamsApp.views.server_error'


urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    url(r'^clients$', views.clients, name='clients'),
    url(r'^clientSave$', views.save_client, name='save_client'),
    url(r'^clientEdit$', views.edit_client, name='edit_client'),
    url(r'^clientDelete$', views.delete_client, name='delete_client'),
    url(r'^client$', views.client_profile),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^ivgetTypes$', views.get_intervention_types),
    url(r'^ivSave$', views.save_intervention),
    url(r'^ivList$', views.get_intervention_list),
    url(r'^ivGet$', views.get_intervention),
    url(r'^ivUpdate$', views.update_intervention),
    url(r'^ivDelete$', views.delete_intervention),
    url(r'^intervention$', views.testajax),
    url(r'^getSubCounties$', views.get_sub_counties),
    url(r'^getWards$', views.get_wards),
    url(r'^logout$', views.log_me_out),
    url(r'^reporting$', views.reporting, name='reporting'),
    url(r'^help$', views.user_help, name='user_help'),
    url(r'^help/download/$', views.user_help_download, name='user_help_download'),
    url(r'^logs$', views.logs, name='logs'),
    url(r'^admin/users$', views.users, name='users'),
    url(r'^admin/users/save$', views.save_user, name='new user'),
    url(r'^admin/users/change_cred$', views.change_cred, name='change_cred'),
    url(r'^admin/users/toggle_status$', views.toggle_status, name='toggle_user_status'),
    url(r'^grievances$', views.grievances_list, name='grievances'),
    url(r'^grievances/create$', views.grievances_create, name='grievances_create'),
    url(r'^grievances/edit', views.grievances_edit, name='grievances_edit'),
    url(r'^grievances/delete', views.grievances_delete, name='grievances_delete'),
    url(r'^grievances/get', views.grievances_get, name='grievances_get'),
    url(r'^cashTransfer/save', views.cash_transfer_details_save, name='cash_transfer_details_save'),
    url(r'^excel-output', views.download_excel, name='excel_template'),
    url(r'^download-excel/$', views.downloadEXCEL),
    url(r'^download-intervention-excel/$', views.downloadRawInterventionEXCEL),
    url(r'^export-page', views.export_page),
    url(r'^intervention-export-page', views.intervention_export_page),
    url(r'^service-layering-export-page', views.individual_service_layering_export_page),
    url(r'^download-service-layering-excel/$', views.downloadIndividualLayeringReport),
    url(r'^client_baseline_info', views.viewBaselineData),
    url(r'^update-demographics', views.update_demographics_data),
    url(r'^update-individual-household', views.update_individual_and_household_data),
    url(r'^update-education-employment', views.update_edu_and_employment_data),
    url(r'^update-hiv-testing', views.update_hiv_testing_data),
    url(r'^update-sexuality', views.update_sexuality_data),
    url(r'^update-reproductive-health', views.update_rep_health_data),
    url(r'^update-gbv', views.update_gbv_data),
    url(r'^update-drug-use', views.update_drug_use_data),
    url(r'^update-programme-participation', views.update_programme_participation_data),
    url(r'^client/exit$', views.client_exit_status_toggle),
    url(r'^client/transfer$', views.transfer_client, name='transfer_client'),
    url(r'^client-transfers$', views.client_transfers, name='client_transfers'),
    url(r'^accept-client-transfer$', views.accept_client_transfer, name='accept_client_transfer'),
    url(r'^reject-client-transfer$', views.reject_client_transfer, name='reject_client_transfer'),
    url(r'^get-client-transfers-count$', views.get_client_transfers_count, name='get_client_transfers_count'),

    #url(r'^$', views.user_login, name='login'),
    url(r'^', views.error_404, name='error_404'),
]
