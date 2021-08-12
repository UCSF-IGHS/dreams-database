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

from django.conf.urls import url, include
from django.contrib import admin
from DreamsApp import views
from DreamsApp.api import urls

urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    url(r'^clients$', views.ClientListView.as_view(), name='clients'),
    url(r'^clientSave$', views.ClientCreateView.as_view(), name='save_client'),
    url(r'^clientEdit$', views.ClientUpdateView.as_view(), name='edit_client'),  ## NOT USED IN APPLICATION
    url(r'^clientDelete$', views.ClientDeleteView.as_view(), name='delete_client'),  ## NOT USED IN APPLICATION
    url(r'^client$', views.client_profile),
    url(r'^follow_ups$', views.follow_ups, name='follow_ups'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^ivgetTypes$', views.get_intervention_types),
    url(r'^ivgetType$', views.get_intervention_type),
    url(r'^getExternalOrganisations$', views.get_external_organisation),
    url(r'^getExitReasons', views.get_exit_reasons),
    url(r'^getInterventionTypes$', views.get_all_intervention_types),
    url(r'^getImplementingPartners$', views.get_implementing_partners),
    url(r'^initiateReferral$', views.initiate_referral),
    url(r'^getMinMaxDateOfBirth', views.get_min_max_date_of_birth),
    url(r'^getUnsuccessfulFollowUpAttempts$', views.get_unsuccessful_followup_attempts),
    url(r'^ivSave$', views.save_intervention),
    url(r'^ivList$', views.get_intervention_list),
    url(r'^ivGet$', views.get_intervention),
    url(r'^ivUpdate$', views.update_intervention),
    url(r'^editFollowUp$', views.update_follow_up),
    url(r'^ivDelete$', views.delete_intervention),
    url(r'^deleteFollowUp$', views.delete_follow_up),
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
    url(r'^download-enrollment-report/$', views.download_raw_enrollment_export),
    url(r'^download-intervention-export/$', views.download_raw_intervention_export),
    url(r'^export-page', views.export_page),
    url(r'^intervention-export-page', views.intervention_export_page),
    url(r'^service-layering-export-page', views.individual_service_layering_export_page),
    url(r'^download-service-layering-report/$', views.download_services_received_export),
    url(r'^client_baseline_info', views.ClientDetailView.as_view()),

    # URLs for ajax to populate related client info individually
    url(r'^client_household_info', views.householdview),
    url(r'^education_employment_info', views.educationemploymentview),
    url(r'^hiv_testing_info', views.hivtestingview),
    url(r'^sexuality_info', views.sexualityview),
    url(r'^reproductive_health_info', views.reproductivehealthview),
    url(r'^gbv_info', views.gbvview),
    url(r'^drug_use_info', views.druguseview),
    url(r'^participation_in_program_info', views.participationinprogramview),

    url(r'^update-demographics', views.ClientDemographicsCreateUpdateView.as_view()),
    url(r'^update-individual-household', views.IndividualHouseHoldCreateUpdateView.as_view()),
    url(r'^update-education-employment', views.EducationAndEmploymentCreateUpdateView.as_view()),
    url(r'^update-hiv-testing', views.HIVTestingCreateUpdateView.as_view()),
    url(r'^update-sexuality', views.SexualityCreateUpdateView.as_view()),
    url(r'^update-reproductive-health', views.ReproductiveHealthCreateUpdateView.as_view()),
    url(r'^update-gbv', views.GenderBasedViolenceCreateUpdateView.as_view()),
    url(r'^update-drug-use', views.DrugUseCreateUpdateView.as_view()),
    url(r'^update-programme-participation', views.ProgramParticipationCreateUpdateView.as_view()),
    url(r'^client/exit$', views.exit_client),
    url(r'^client/unexit$', views.unexit_client),
    url(r'^client/transfer$', views.transfer_client, name='transfer_client'),
    url(r'^client-transfers/(?P<transferred_in>[0-1])$', views.client_transfers, name='client_transfers'),
    url(r'^client-referrals/(?P<referred_in>[0-1])$', views.ClientReferralsListView.as_view(), name='client_referrals'),
    url(r'^accept-client-transfer$', views.accept_client_transfer, name='accept_client_transfer'),
    url(r'^reject-client-transfer$', views.reject_client_transfer, name='reject_client_transfer'),
    url(r'^reject-client-referral$', views.reject_client_referral, name='reject_client_referral'),
    url(r'^get-pending-client-transfers-total-count$', views.get_pending_client_transfers_total_count,
        name='get_pending_client_transfers_total_count'),
    url(r'^get-pending-client-transfers-in-out-count$', views.get_pending_client_transfers_in_out_count,
        name='get_pending_client_transfers_in_out_count'),
    url(r'^get-pending-client-referrals-total-count$', views.get_pending_client_referrals_total_count,
        name='get_pending_client_referrals_total_count'),
    url(r'^get-pending-client-referrals-in-out-count$', views.get_pending_client_referrals_in_out_count,
        name='get_pending_client_referrals_in_out_count'),
    url(r'^intervention-export-transferred-in-page', views.intervention_export_transferred_in_page,
        name='intervention_export_transferred_in_page'),
    url(r'^download-intervention-transferred-in-report/$', views.download_raw_intervention_transferred_in_export,
        name='download_intervention_transferred_in_report'),
    url(r'^client/void$', views.void_client, name='void_client'),
    url(r'^export-client-transfers/(?P<transferred_in>[0-1])$', views.export_client_transfers,
        name='export_client_transfers'),
    url(r'^export-client-referrals/(?P<referred_in>[0-1])$', views.export_client_referrals,
        name='export_client_referrals'),
    url(r'^download-audit-logs', views.download_audit_logs,
        name='download_audit_logs'),
    url(r'^addFollowUp$', views.add_follow_up),
]

urlpatterns += urls.urlpatterns

handler404 = views.page_not_found
handler400 = views.bad_request
handler403 = views.permission_denied
handler500 = views.server_error
