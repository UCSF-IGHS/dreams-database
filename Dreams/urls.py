# coding=utf-8
"""Dreams URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin
from DreamsApp import views
from DreamsApp.api import urls

urlpatterns = [
    path('', views.user_login, name='login'),
    path('clients', views.ClientListView.as_view(), name='clients'),
    path('clientSave', views.ClientCreateView.as_view(), name='save_client'),
    path('clientEdit', views.ClientUpdateView.as_view(), name='edit_client'),
    path('clientDelete', views.ClientDeleteView.as_view(), name='delete_client'),
    path('client', views.client_profile),
    path('follow_ups', views.FollowUpsListView.as_view(), name='follow_ups'),
    path('admin/', admin.site.urls, name='admin'),
    path('ivgetTypes', views.get_intervention_types),
    path('ivgetType', views.get_intervention_type),
    path('getExternalOrganisations', views.get_external_organisation),
    path('getExitReasons', views.get_exit_reasons),
    path('getInterventionTypes', views.get_all_intervention_types),
    path('getImplementingPartners', views.get_implementing_partners),
    path('initiateReferral', views.initiate_referral),
    path('getMinMaxDateOfBirth', views.get_min_max_date_of_birth),
    path('getUnsuccessfulFollowUpAttempts', views.get_unsuccessful_followup_attempts),
    path('ivSave', views.save_intervention),
    path('ivList', views.get_intervention_list),
    path('ivGet', views.get_intervention),
    path('ivUpdate', views.update_intervention),
    path('editFollowUp', views.update_follow_up),
    path('ivDelete', views.delete_intervention),
    path('deleteFollowUp', views.delete_follow_up),
    path('intervention', views.testajax),
    path('getSubCounties', views.get_sub_counties),
    path('getWards', views.get_wards),
    path('logout', views.log_me_out),
    path('reporting', views.reporting, name='reporting'),
    path('help', views.user_help, name='user_help'),
    path('help/download/', views.user_help_download, name='user_help_download'),
    path('logs', views.logs, name='logs'),
    path('users', views.users, name='users'),
    path('users/save', views.save_user, name='new user'),
    path('users/change_cred', views.change_cred, name='change_cred'),
    path('users/toggle_status', views.toggle_status, name='toggle_user_status'),
    path('grievances', views.GrievancesListView.as_view(), name='grievances'),
    path('grievances/create', views.grievances_create, name='grievances_create'),
    path('grievances/edit', views.grievances_edit, name='grievances_edit'),
    path('grievances/delete', views.grievances_delete, name='grievances_delete'),
    path('grievances/get', views.grievances_get, name='grievances_get'),
    path('cashTransfer/save', views.cash_transfer_details_save, name='cash_transfer_details_save'),
    path('download-enrollment-report/', views.download_raw_enrollment_export),
    path('download-intervention-export/', views.download_raw_intervention_export),
    path('export-page', views.export_page),
    path('intervention-export-page', views.intervention_export_page),
    path('service-layering-export-page', views.individual_service_layering_export_page),
    path('download-service-layering-report/', views.download_services_received_export),
    path('client_baseline_info', views.ClientDetailView.as_view()),

    # URLs for ajax to populate related client info individually
    path('client_household_info', views.householdview),
    path('education_employment_info', views.educationemploymentview),
    path('hiv_testing_info', views.hivtestingview),
    path('sexuality_info', views.sexualityview),
    path('reproductive_health_info', views.reproductivehealthview),
    path('gbv_info', views.gbvview),
    path('drug_use_info', views.druguseview),
    path('participation_in_program_info', views.participationinprogramview),

    path('update-demographics', views.ClientDemographicsCreateUpdateView.as_view()),
    path('update-individual-household', views.IndividualHouseHoldCreateUpdateView.as_view()),
    path('update-education-employment', views.EducationAndEmploymentCreateUpdateView.as_view()),
    path('update-hiv-testing', views.HIVTestingCreateUpdateView.as_view()),
    path('update-sexuality', views.SexualityCreateUpdateView.as_view()),
    path('update-reproductive-health', views.ReproductiveHealthCreateUpdateView.as_view()),
    path('update-gbv', views.GenderBasedViolenceCreateUpdateView.as_view()),
    path('update-drug-use', views.DrugUseCreateUpdateView.as_view()),
    path('update-programme-participation', views.ProgramParticipationCreateUpdateView.as_view()),
    path('client/exit', views.exit_client),
    path('client/unexit', views.unexit_client),
    path('client/transfer', views.transfer_client, name='transfer_client'),
    path('client-transfers/<int:transferred_in>/', views.ClientTransfesListView.as_view(), name='client_transfers'),
    path('client-referrals/<int:referred_in>/', views.ClientReferralsListView.as_view(), name='client_referrals'),
    path('accept-client-transfer', views.accept_client_transfer, name='accept_client_transfer'),
    path('reject-client-transfer', views.reject_client_transfer, name='reject_client_transfer'),
    path('reject-client-referral', views.reject_client_referral, name='reject_client_referral'),
    path('get-pending-client-transfers-total-count', views.get_pending_client_transfers_total_count,
        name='get_pending_client_transfers_total_count'),
    path('get-pending-client-transfers-in-out-count', views.get_pending_client_transfers_in_out_count,
        name='get_pending_client_transfers_in_out_count'),
    path('get-pending-client-referrals-total-count', views.get_pending_client_referrals_total_count,
        name='get_pending_client_referrals_total_count'),
    path('get-pending-client-referrals-in-out-count', views.get_pending_client_referrals_in_out_count,
        name='get_pending_client_referrals_in_out_count'),
    path('intervention-export-transferred-in-page', views.intervention_export_transferred_in_page,
        name='intervention_export_transferred_in_page'),
    path('download-intervention-transferred-in-report/', views.download_raw_intervention_transferred_in_export,
        name='download_intervention_transferred_in_report'),
    path('client/void', views.void_client, name='void_client'),
    path('export-client-transfers/<int:transferred_in>/', views.export_client_transfers,
        name='export_client_transfers'),
    path('export-client-referrals/<int:referred_in>/', views.export_client_referrals,
        name='export_client_referrals'),
    path('download-audit-logs', views.download_audit_logs,
        name='download_audit_logs'),
    path('addFollowUp', views.add_follow_up),
]

urlpatterns += urls.urlpatterns

handler404 = views.page_not_found
handler400 = views.bad_request
handler403 = views.permission_denied
handler500 = views.server_error
