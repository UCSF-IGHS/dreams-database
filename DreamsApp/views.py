import os
import traceback
from functools import reduce

import unicodecsv
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseServerError, HttpResponse
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.exceptions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.cache import cache
from django.db import connection as db_conn_2, transaction
from django.utils.timezone import make_aware
import urllib.parse
import json
from datetime import date, timedelta, datetime as dt
from DreamsApp.Dreams_Utils_Plain import DreamsRawExportTemplateRenderer, settings
from DreamsApp.business_rules.model_access_permissions.client_access_permissions import ClientActionPermissions
from DreamsApp.business_rules.model_access_permissions.intervention_access_permissions import \
    InterventionActionPermissions
from DreamsApp.business_rules.services.query_services.client_query_service import ClientQueryService
from DreamsApp.forms import *
from dateutil.relativedelta import relativedelta
from DreamsApp.service_layer import ClientEnrolmentServiceLayer, TransferServiceLayer, ReferralServiceLayer, \
    FollowUpsServiceLayer
from operator import itemgetter
import operator
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView


def get_enrollment_form_config_data(request):
    try:
        try:
            current_ip = request.user.implementingpartneruser.implementing_partner.code
        except Exception as e:
            current_ip = 0
        config_data = {
            'implementing_partners': ImplementingPartner.objects.all(),
            'verification_documents': VerificationDocument.objects.all(),
            'marital_status': MaritalStatus.objects.all(),
            'counties': County.objects.all(),
            'current_ip': current_ip
        }
        return config_data
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def log_custom_actions(user_id, table, row_id, action, search_text):
    try:
        audit = Audit()
        audit.user_id = user_id
        audit.table = table
        audit.row_id = row_id
        audit.action = action
        audit.search_text = search_text
        audit.save()
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def user_login(request):
    try:
        if request.user.is_authenticated():
            return redirect('clients')
        if request.method == 'GET':
            return render(request, 'login.html', {'page_title': 'Login', 'page': 'login'})
        elif request.method == 'POST':
            user_name = request.POST.get('inputUsername', '')
            pass_word = request.POST.get('inputPassword', '')

            audit = Audit()
            audit.user_id = 0
            audit.table = "DreamsApp_client"
            audit.row_id = 0
            audit.action = "LOGIN"

            if user_name == '' or pass_word == '':
                audit.search_text = "Missing login Credentials"
                audit.save()
                response_data = {
                    'status': 'fail',
                    'message': 'Missing username or password.',
                    'page': 'login',
                    'page_title': 'Login'
                }
            else:
                user = authenticate(username=user_name, password=pass_word)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        audit.user_id = user.id
                        audit.search_text = "Login Successful for username: " + user_name
                        audit.save()
                        response_data = {
                            'status': 'success',
                            'message': 'Login successfull'
                        }
                    else:
                        audit.search_text = "Failed login for username: " + user_name
                        audit.save()
                        response_data = {
                            'status': 'fail',
                            'message': 'Sorry, your account is disabled'
                        }
                else:
                    response_data = {
                        'status': 'fail',
                        'message': 'Incorrect username or password'
                    }
            return JsonResponse(json.dumps(response_data), safe=False)
        else:
            return render(request, 'login.html')
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def build_filter_client_queryset(turple_1, turple_2, turple_3, turple_4, turple_5, turple_6):
    try:
        return Client.objects.filter(Q(first_name__icontains=str(turple_1[0]), middle_name__icontains=str(turple_1[1]),
                                       last_name__icontains=str(turple_1[2])) |
                                     Q(first_name__icontains=str(turple_2[0]), middle_name__icontains=str(turple_2[1]),
                                       last_name__icontains=str(turple_2[2])) |
                                     Q(first_name__icontains=str(turple_3[0]), middle_name__icontains=str(turple_3[1]),
                                       last_name__icontains=str(turple_3[2])) |
                                     Q(first_name__icontains=str(turple_4[0]), middle_name__icontains=str(turple_4[1]),
                                       last_name__icontains=str(turple_4[2])) |
                                     Q(first_name__icontains=str(turple_5[0]), middle_name__icontains=str(turple_5[1]),
                                       last_name__icontains=str(turple_5[2])) |
                                     Q(first_name__icontains=str(turple_6[0]), middle_name__icontains=str(turple_6[1]),
                                       last_name__icontains=str(turple_6[2]))) \
            .exclude(voided=True) \
            .order_by('first_name') \
            .order_by('middle_name') \
            .order_by('last_name')
    except Exception as e:
        return Client.objects.all()[0]


def filter_clients(search_client_term, is_advanced_search, request):
    search_client_term_parts = search_client_term.split()
    # check number of parts
    parts_count = len(search_client_term_parts)
    cache_key = '-'.join(search_client_term_parts)  # needs to be unique
    cache_time = 86400  # time in seconds for cache to be valid
    search_result = None

    if parts_count == 1:
        search_result = client_filter_with_one_search_part(search_client_term_parts[0])
    elif parts_count > 1:
        search_result = client_filter_with_multiple_search_parts(search_client_term_parts, parts_count)
    if is_advanced_search == 'True':
        data = client_advanced_search(search_result, is_advanced_search, request)
        return data

    cache.set(cache_key, search_result, cache_time)
    return [search_result, is_advanced_search, '', '', '', '', '']


def client_filter_with_one_search_part(search_client_part):
    data = cache.get(search_client_part)  # returns None if no key-value pair
    if not data:
        search_result = Client.objects.filter(Q(dreams_id__iexact=search_client_part) |
                                              Q(first_name__iexact=search_client_part) |
                                              Q(middle_name__iexact=search_client_part) |
                                              Q(last_name__iexact=search_client_part)) \
            .exclude(voided=True).order_by('first_name').order_by('middle_name').order_by('last_name')
        data = search_result
    return data


def client_filter_with_multiple_search_parts(search_client_term_parts, parts_count):
    data = cache.get('-'.join(search_client_term_parts))
    if not data:
        # this is not a dreams id search but a name search
        filter_text_1 = search_client_term_parts[0]
        filter_text_2 = search_client_term_parts[1]
        filter_text_3 = '' if parts_count == 2 else search_client_term_parts[2]
        # first name and middle name
        data = build_filter_client_queryset((filter_text_1, filter_text_2, filter_text_3),
                                            (filter_text_2, filter_text_1, filter_text_3),
                                            (filter_text_2, filter_text_3, filter_text_1),
                                            (filter_text_3, filter_text_2, filter_text_1),
                                            (filter_text_3, filter_text_1, filter_text_2),
                                            (filter_text_1, filter_text_3, filter_text_2))
    return data


def client_advanced_search(search_result, is_advanced_search, request):
    county_filter = str(
        request.GET.get('county', '') if request.method == 'GET' else request.POST.get('county', ''))
    if county_filter != '':
        search_result = search_result.filter(county_of_residence_id=int(county_filter))
    sub_county_filter = str(
        request.GET.get('sub_county', '') if request.method == 'GET' else request.POST.get('sub_county', ''))
    if sub_county_filter != '':
        search_result = search_result.filter(sub_county_id=int(sub_county_filter))
    ward_filter = str(request.GET.get('ward', '') if request.method == 'GET' else request.POST.get('ward', ''))
    if ward_filter != '':
        search_result = search_result.filter(ward_id=int(ward_filter))
    start_date_filter_original = request.GET.get('doe_start_filter',
                                                 '') if request.method == 'GET' else request.POST.get(
        'doe_start_filter', '')
    start_date_filter = '2015-10-01' if start_date_filter_original == '' else start_date_filter_original
    end_date_filter_original = request.GET.get('doe_end_filter',
                                               dt.today()) if request.method == 'GET' else request.POST.get(
        'doe_end_filter', dt.today())
    end_date_filter = dt.today() if end_date_filter_original == '' else end_date_filter_original
    search_result = search_result.filter(date_of_enrollment__range=[start_date_filter, end_date_filter])  #
    return [search_result, is_advanced_search, county_filter, sub_county_filter, ward_filter,
            start_date_filter_original,
            end_date_filter_original]


class ClientListView(ListView):
    model = Client
    template_name = 'clients.html'

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['page'] = 'clients'
        context['page_title'] = 'DREAMS Client List'
        context['status'] = 'success'
        # context['implementing_partners'] = ImplementingPartner.objects.all()
        # context['verification_documents'] = VerificationDocument.objects.all()
        # ['marital_status'] = MaritalStatus.objects.all()
        context['counties'] = County.objects.all()
        context['demo_form'] = DemographicsForm()
        context['to_login'] = False
        context['error'] = ''

        try:
            user = self.request.user
            if user is not None and user.is_authenticated() and user.is_active:
                # get search details -- search_client_term
                page = self.request.GET.get('page', 1) if self.request.method == 'GET' else self.request.POST.get(
                    'page', 1)
                is_advanced_search = self.request.GET.get('is_advanced_search',
                                                          'False') if self.request.method == 'GET' else self.request.POST.get(
                    'is_advanced_search', 'False')
                search_client_term = self.request.GET.get('search_client_term',
                                                          '') if self.request.method == 'GET' else self.request.POST.get(
                    'search_client_term', '')
                search_client_term = search_client_term.strip()

                ip_user = None
                try:
                    ip_user = user.implementingpartneruser
                    current_ip = ip_user.implementing_partner.code

                except Exception as e:
                    if not ip_user:
                        context['error'] = "You do not belong to any implementing partners"
                        return context
                    current_ip = 0

                if search_client_term != "":
                    client_query_service = ClientQueryService(ip_user)
                    search_criteria = get_search_criteria(search_client_term, is_advanced_search, self.request)
                    try:
                        result = client_query_service.search_clients(search_criteria)
                    except Client.DoesNotExist as e:
                        result = Client.objects.none()

                    search_result = result.order_by('first_name', 'middle_name', 'last_name')[:100]
                    ## EXCLUDE DELEGATION
                    # search_result_tuple = filter_clients(search_client_term, is_advanced_search, request)

                    search_result_length = len(search_result)
                    a = 'True' if search_result_length >= 100 else 'False'
                    search_result_tuple = [search_result, a, '', '', '', '', '']

                    log_custom_actions(user.id, "DreamsApp_client", None, "SEARCH", search_client_term)

                    client_action_permissions = ClientActionPermissions(model=Client, user=user)
                    intervention_action_permissions = InterventionActionPermissions(model=Intervention,
                                                                                    user=user)
                    display_first_100_clients = (search_result_length == 100)

                    # if request.is_ajax():
                    #     enrolment_results = [
                    #         [ClientActionPermissions(model=Client, user=request.user, enrolment=client), client] for
                    #         client
                    #         in search_result]
                    #
                    #     json_response = {
                    #         'search_result': serializers.serialize('json', enrolment_results),
                    #         'search_client_term': search_client_term,
                    #         'can_manage_client': request.user.has_perm('auth.can_manage_client'),
                    #         'can_change_client': request.user.has_perm('auth.can_change_client'),
                    #         'can_delete_client': request.user.has_perm('auth.can_delete_client'),
                    #         'implementing_partners': ImplementingPartner.objects.all(),
                    #         'verification_documents': VerificationDocument.objects.all(),
                    #         'marital_status': MaritalStatus.objects.all(),
                    #         'counties': County.objects.all(),
                    #         'current_ip': current_ip,
                    #         'demo_form': DemographicsForm(),
                    #         'client_action_permissions': client_action_permissions,
                    #         'intervention_action_permissions': intervention_action_permissions,
                    #         'display_first_100_clients': display_first_100_clients
                    #     }
                    #     return JsonResponse(json_response, safe=False)
                    # else:

                    # Non ajax request.. Do a paginator
                    # do pagination
                    enrolment_results = [
                        [ClientActionPermissions(model=Client, user=user, enrolment=client), client] for client in
                        search_result]

                    try:
                        paginator = Paginator(enrolment_results, 20)
                        client_paginator = paginator.page(page)
                    except PageNotAnInteger:
                        client_paginator = paginator.page(1)  # Deliver the first page is page is not an integer
                    except EmptyPage:
                        client_paginator = paginator.page(
                            paginator.num_pages)  # Deliver the last page if page is out of scope

                    ### EXCLUDE DELEGATION
                    # county_filter = search_result_tuple[2] if search_result_tuple[2] != '' else '0'
                    # sub_county_filter = search_result_tuple[3] if search_result_tuple[3] != '' else '0'
                    # sub_counties = SubCounty.objects.filter(county_id=int(county_filter))
                    # ward_filter = search_result_tuple[4] if search_result_tuple[4] != '' else '0'
                    # wards = Ward.objects.filter(sub_county_id=int(sub_county_filter))

                    client_enrolment_service_layer = ClientEnrolmentServiceLayer(user)
                    minimum_maximum_age = client_enrolment_service_layer.get_minimum_maximum_enrolment_age(
                        client_enrolment_service_layer.ENROLMENT_CUTOFF_DATE)
                    max_dob = dt.now().date() - relativedelta(years=int(minimum_maximum_age[0]))
                    min_dob = dt.now().date() - relativedelta(
                        years=int(minimum_maximum_age[1]) + 1) + timedelta(
                        days=1)

                    context['search_client_term'] = search_client_term
                    context['client_paginator'] = client_paginator
                    context['current_ip'] = current_ip
                    context['is_advanced_search'] = search_result_tuple[1]
                    # 'county_filter': county_filter,
                    # 'sub_county_filter': sub_county_filter,
                    # 'sub_counties': sub_counties,
                    # 'ward_filter': ward_filter,
                    # 'wards': wards,
                    context['start_date_filter'] = search_result_tuple[5]
                    context['end_date_filter'] = search_result_tuple[6]
                    context['max_dob'] = max_dob
                    context['min_dob'] = min_dob
                    context['result_list'] = enrolment_results
                    context['client_action_permissions'] = client_action_permissions
                    context['intervention_action_permissions'] = intervention_action_permissions
                    context['display_first_100_clients'] = display_first_100_clients
                else:
                    search_result = Client.objects.none()
                    search_result_tuple = [search_result, 'False', '', '', '', '', '']

                    client_action_permissions = ClientActionPermissions(model=Client, user=user)
                    # intervention_action_permissions = InterventionActionPermissions(model=Intervention, user=request.user)
                    client_enrolment_service_layer = ClientEnrolmentServiceLayer(user)
                    minimum_maximum_age = client_enrolment_service_layer.get_minimum_maximum_enrolment_age(
                        client_enrolment_service_layer.ENROLMENT_CUTOFF_DATE)
                    max_dob = datetime.now().date() - relativedelta(years=int(minimum_maximum_age[0]))
                    min_dob = datetime.now().date() - relativedelta(years=int(minimum_maximum_age[1]) + 1) + timedelta(
                        days=1)

                    context['search_client_term'] = search_client_term
                    # 'client_paginator': client_paginator,
                    context['current_ip'] = current_ip
                    context['is_advanced_search'] = search_result_tuple[1]
                    # 'county_filter': county_filter,
                    # 'sub_county_filter': sub_county_filter,
                    # 'sub_counties': sub_counties,
                    # 'ward_filter': ward_filter,
                    # 'wards': wards,
                    # 'start_date_filter': search_result_tuple[5],
                    # 'end_date_filter': search_result_tuple[6],
                    context['max_dob'] = max_dob
                    context['min_dob'] = min_dob
                    # 'result_list': enrolment_results,
                    context['client_action_permissions'] = client_action_permissions
                    # 'intervention_action_permissions': intervention_action_permissions
                    # 'display_first_100_clients': display_first_100_clients

            else:
                context['to_login'] = True
            # print(len(db_conn_2.queries))

        except Exception as e:
            tb = traceback.format_exc(e)
            context['error'] = tb
        return context

    def render_to_response(self, context, **response_kwargs):
        if context['to_login']:
            return redirect('login')
        if context['error'] != '':
            return HttpResponseServerError(context['error'])
        return super(ClientListView, self).render_to_response(context, **response_kwargs)

    def get_queryset(self):
        return Client.objects.none()


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client_baseline_data.html'

    def get_object(self, queryset=None):
        try:
            client_id = int(self.request.GET['client_id'])
            if client_id is not None and client_id != 0:
                self.object = Client.objects.get(id=client_id, voided=False)
        except Exception as e:
            self.object = None
        return self.object

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['page'] = 'clients'
        context['page_title'] = 'DREAMS Enrollment Data'
        context['user'] = self.request.user
        context['to_login'] = False
        context['error'] = ''

        """ Returns client profile """
        user = self.request.user
        if user is None or not user.is_authenticated() or not user.is_active:
            context['to_login'] = True
            return context

        if self.request.method != 'GET':
            context['error'] = 'POST not allowed'
            return context

        try:
            client_demographics = self.object
            if not client_demographics:
                context['error'] = "Client does not exist"
                return context

            # Relation is a one-to-one to Client
            # Consider client = models.OneToOneField(Client, db_index=True)
            # instead of client = models.ForeignKey(Client, db_index=True)
            # then below: client_demographics.clientindividualandhouseholddata
            demographics_form = DemographicsForm(instance=client_demographics)
            search_client_term = self.request.GET.get('search_client_term', '')

            ip_user = None
            try:
                ip_user = user.implementingpartneruser
            except Exception as e:
                if not ip_user:
                    context['error'] = "You do not belong to any implementing partners"
                    return context

            ip = ip_user.implementing_partner
            ip_code = ip.code if ip else None

            is_editable_by_ip = client_demographics.is_editable_by_ip(ip)
            client_status = client_demographics.get_client_status(ip)
            date_of_enrollment_str = demographics_form['date_of_enrollment'].value()
            date_of_enrollment = datetime.strptime(str(date_of_enrollment_str),
                                                   '%Y-%m-%d').date() if date_of_enrollment_str is not None else dt.now().date()
            client_enrolment_service_layer = ClientEnrolmentServiceLayer(user)
            minimum_maximum_age = client_enrolment_service_layer.get_minimum_maximum_enrolment_age(
                client_enrolment_service_layer.ENROLMENT_CUTOFF_DATE)
            max_dob = date_of_enrollment - relativedelta(years=int(minimum_maximum_age[0]))
            min_dob = date_of_enrollment - relativedelta(years=int(minimum_maximum_age[1]) + 1) + timedelta(days=1)
            current_user_belongs_to_same_ip_as_client = client_demographics.current_user_belongs_to_same_ip_as_client(
                ip_user.implementing_partner_id)
            client_action_permissions = ClientActionPermissions(model=Client, user=user,
                                                                enrolment=client_demographics)
            client_action_permissions.can_perform_edit()

            context['client'] = client_demographics
            context['demo_form'] = demographics_form
            context['search_client_term'] = search_client_term
            context['transfer_form'] = ClientTransferForm(
                ip_code=ip_code,
                initial={'client': client_demographics})
            context['is_editable_by_ip'] = is_editable_by_ip
            context['client_status'] = client_status
            context['max_dob'] = max_dob
            context['min_dob'] = min_dob
            context[
                'current_user_belongs_to_same_ip_as_client'] = current_user_belongs_to_same_ip_as_client or user.is_superuser
            context['client_action_permissions'] = client_action_permissions

        except Client.DoesNotExist:
            context['error'] = "Client does not exist"
        except Exception as e:
            context['error'] = traceback.format_exc()
        return context

    def render_to_response(self, context, **response_kwargs):
        if context['to_login']:
            return redirect('login')
        if context['error'] != '':
            # return HttpResponseServerError(context['error'])
            return redirect('clients')
        return super(ClientDetailView, self).render_to_response(context, **response_kwargs)

    def get_queryset(self):
        return Client.objects.none()


def householdview(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            user = request.user
            if user is None or not user.is_authenticated() or not user.is_active:
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            client_id = request.POST.get('client_id', None)
            if client_id is None or client_id == "0":
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail'
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

            client = Client.objects.get(id=int(client_id), voided=False)
            client_household_queryset = client.clientindividualandhouseholddata_set
            client_household = client_household_queryset.get() if client_household_queryset.exists() else None

            household_form = IndividualAndHouseholdForm(instance=client_household)
            household_form.fields["client"].initial = client

            client_action_permissions = ClientActionPermissions(model=ClientIndividualAndHouseholdData,
                                                                user=user, enrolment=client)
            client_action_permissions.can_perform_edit()

            is_editable_by_ip = client.is_editable_by_ip(ip)

            response_data = {
                'status': 'success',
                'household_form': household_form,
                'client_action_permissions': client_action_permissions,
                'is_editable_by_ip': is_editable_by_ip
            }

            template = render_to_string('client_individual_household_form.html', context=response_data, request=request)
            return JsonResponse({"household_form": template})

    except Exception as e:
        response_data = {
            'status': 'fail'
        }
        template = render_to_string('client_individual_household_form.html', context=response_data, request=request)
        return JsonResponse({"household_form": template})


def educationemploymentview(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            user = request.user
            if user is None or not user.is_authenticated() or not user.is_active:
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            client_id = request.POST.get('client_id', None)
            if client_id is None or client_id == "0":
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail'
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

            client = Client.objects.get(id=int(client_id), voided=False)
            client_edu_queryset = client.clienteducationandemploymentdata_set
            client_edu = client_edu_queryset.get() if client_edu_queryset.exists() else None

            edu_form = EducationAndEmploymentForm(instance=client_edu)
            edu_form.fields["client"].initial = client

            client_action_permissions = ClientActionPermissions(model=ClientEducationAndEmploymentData,
                                                                user=user, enrolment=client)
            client_action_permissions.can_perform_edit()

            is_editable_by_ip = client.is_editable_by_ip(ip)

            response_data = {
                'status': 'success',
                'edu_form': edu_form,
                'client_action_permissions': client_action_permissions,
                'is_editable_by_ip': is_editable_by_ip
            }

            template = render_to_string('education_and_employment_form.html', context=response_data, request=request)
            return JsonResponse({"edu_form": template})

    except Exception as e:
        response_data = {
            'status': 'fail'
        }
        template = render_to_string('education_and_employment_form.html', context=response_data, request=request)
        return JsonResponse({"edu_form": template})


def hivtestingview(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            user = request.user
            if user is None or not user.is_authenticated() or not user.is_active:
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            client_id = request.POST.get('client_id', None)
            if client_id is None or client_id == "0":
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail'
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

            client = Client.objects.get(id=int(client_id), voided=False)
            client_hiv_data_queryset = client.clienthivtestingdata_set
            client_hiv_data = client_hiv_data_queryset.get() if client_hiv_data_queryset.exists() else None

            hiv_form = HivTestForm(instance=client_hiv_data)
            hiv_form.fields["client"].initial = client

            client_action_permissions = ClientActionPermissions(model=ClientHIVTestingData, user=user,
                                                                enrolment=client)
            client_action_permissions.can_perform_edit()

            is_editable_by_ip = client.is_editable_by_ip(ip)

            response_data = {
                'status': 'success',
                'hiv_form': hiv_form,
                'client_action_permissions': client_action_permissions,
                'is_editable_by_ip': is_editable_by_ip
            }

            template = render_to_string('client_hiv_testing_form.html', context=response_data, request=request)
            return JsonResponse({"hiv_form": template})

    except Exception as e:
        response_data = {
            'status': 'fail'
        }
        template = render_to_string('client_hiv_testing_form.html', context=response_data, request=request)
        return JsonResponse({"hiv_form": template})


def sexualityview(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            user = request.user
            if user is None or not user.is_authenticated() or not user.is_active:
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            client_id = request.POST.get('client_id', None)
            if client_id is None or client_id == "0":
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail'
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

            client = Client.objects.get(id=int(client_id), voided=False)
            client_sexual_data_queryset = client.clientsexualactivitydata_set
            client_sexual_data = client_sexual_data_queryset.get() if client_sexual_data_queryset.exists() else None

            sexuality_form = SexualityForm(instance=client_sexual_data)
            sexuality_form.fields["client"].initial = client

            client_action_permissions = ClientActionPermissions(model=ClientSexualActivityData, user=user,
                                                                enrolment=client)
            client_action_permissions.can_perform_edit()

            is_editable_by_ip = client.is_editable_by_ip(ip)

            response_data = {
                'status': 'success',
                'sexuality_form': sexuality_form,
                'client_action_permissions': client_action_permissions,
                'is_editable_by_ip': is_editable_by_ip
            }

            template = render_to_string('client_sexuality_form.html', context=response_data, request=request)
            return JsonResponse({"sexuality_form": template})

    except Exception as e:
        response_data = {
            'status': 'fail'
        }
        template = render_to_string('client_sexuality_form.html', context=response_data, request=request)
        return JsonResponse({"sexuality_form": template})


def reproductivehealthview(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            user = request.user
            if user is None or not user.is_authenticated() or not user.is_active:
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            client_id = request.POST.get('client_id', None)
            if client_id is None or client_id == "0":
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail'
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

            client = Client.objects.get(id=int(client_id), voided=False)
            client_rh_data_queryset = client.clientreproductivehealthdata_set
            client_rh_data = client_rh_data_queryset.get() if client_rh_data_queryset.exists() else None

            rh_form = ReproductiveHealthForm(instance=client_rh_data)
            rh_form.fields["client"].initial = client

            client_action_permissions = ClientActionPermissions(model=ClientReproductiveHealthData, user=user,
                                                                enrolment=client)
            client_action_permissions.can_perform_edit()

            is_editable_by_ip = client.is_editable_by_ip(ip)

            response_data = {
                'status': 'success',
                'rh_form': rh_form,
                'client_action_permissions': client_action_permissions,
                'is_editable_by_ip': is_editable_by_ip
            }

            template = render_to_string('client_reproductive_health_form.html', context=response_data, request=request)
            return JsonResponse({"rh_form": template})

    except Exception as e:
        response_data = {
            'status': 'fail'
        }
        template = render_to_string('client_reproductive_health_form.html', context=response_data, request=request)
        return JsonResponse({"rh_form": template})


def gbvview(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            user = request.user
            if user is None or not user.is_authenticated() or not user.is_active:
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            client_id = request.POST.get('client_id', None)
            if client_id is None or client_id == "0":
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail'
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

            client = Client.objects.get(id=int(client_id), voided=False)
            client_gbv_data_queryset = client.clientgenderbasedviolencedata_set
            client_gbv_data = client_gbv_data_queryset.get() if client_gbv_data_queryset.exists() else None

            gbv_form = GBVForm(instance=client_gbv_data)
            gbv_form.fields["client"].initial = client

            client_action_permissions = ClientActionPermissions(model=ClientGenderBasedViolenceData, user=user,
                                                                enrolment=client)
            client_action_permissions.can_perform_edit()

            is_editable_by_ip = client.is_editable_by_ip(ip)

            response_data = {
                'status': 'success',
                'gbv_form': gbv_form,
                'client_action_permissions': client_action_permissions,
                'is_editable_by_ip': is_editable_by_ip
            }

            template = render_to_string('client_gbv_form.html', context=response_data, request=request)
            return JsonResponse({"gbv_form": template})

    except Exception as e:
        response_data = {
            'status': 'fail'
        }
        template = render_to_string('client_gbv_form.html', context=response_data, request=request)
        return JsonResponse({"gbv_form": template})


def druguseview(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            user = request.user
            if user is None or not user.is_authenticated() or not user.is_active:
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            client_id = request.POST.get('client_id', None)
            if client_id is None or client_id == "0":
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail'
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

            client = Client.objects.get(id=int(client_id), voided=False)
            client_drug_data_queryset = client.clientdrugusedata_set
            client_drug_data = client_drug_data_queryset.get() if client_drug_data_queryset.exists() else None

            drug_use_form = DrugUseForm(instance=client_drug_data)
            drug_use_form.fields["client"].initial = client

            client_action_permissions = ClientActionPermissions(model=ClientDrugUseData, user=user,
                                                                enrolment=client)
            client_action_permissions.can_perform_edit()

            is_editable_by_ip = client.is_editable_by_ip(ip)

            response_data = {
                'status': 'success',
                'drug_use_form': drug_use_form,
                'client_action_permissions': client_action_permissions,
                'is_editable_by_ip': is_editable_by_ip
            }

            template = render_to_string('client_drug_use_form.html', context=response_data, request=request)
            return JsonResponse({"drug_use_form": template})

    except Exception as e:
        response_data = {
            'status': 'fail'
        }
        template = render_to_string('client_drug_use_form.html', context=response_data, request=request)
        return JsonResponse({"drug_use_form": template})


def participationinprogramview(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            user = request.user
            if user is None or not user.is_authenticated() or not user.is_active:
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            client_id = request.POST.get('client_id', None)
            if client_id is None or client_id == "0":
                response_data = {
                    'status': 'fail',
                    'to_login': True
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail'
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

            client = Client.objects.get(id=int(client_id), voided=False)
            client_prog_part_data_queryset = client.clientparticipationindreams_set
            client_prog_part_data = client_prog_part_data_queryset.get() if client_prog_part_data_queryset.exists() else None

            programe_participation_form = DreamsProgramParticipationForm(instance=client_prog_part_data)
            programe_participation_form.fields["client"].initial = client

            client_action_permissions = ClientActionPermissions(model=ClientParticipationInDreams, user=user,
                                                                enrolment=client)
            client_action_permissions.can_perform_edit()

            is_editable_by_ip = client.is_editable_by_ip(ip)

            response_data = {
                'status': 'success',
                'programe_participation_form': programe_participation_form,
                'client_action_permissions': client_action_permissions,
                'is_editable_by_ip': is_editable_by_ip
            }

            template = render_to_string('client_programme_participation_form.html', context=response_data,
                                        request=request)
            return JsonResponse({"programe_participation_form": template})

    except Exception as e:
        response_data = {
            'status': 'fail'
        }
        template = render_to_string('client_programme_participation_form.html', context=response_data, request=request)
        return JsonResponse({"programe_participation_form": template})


def get_search_criteria(search_client_term, is_advanced_search, request):
    search_criteria = {}

    if search_client_term != '':
        search_criteria['search_text'] = search_client_term

    county_filter = str(
        request.GET.get('county', '') if request.method == 'GET' else request.POST.get('county', ''))
    if county_filter != '' and is_advanced_search:
        search_criteria['county'] = int(county_filter)

    sub_county_filter = str(
        request.GET.get('sub_county', '') if request.method == 'GET' else request.POST.get('sub_county', ''))

    if sub_county_filter != '' and is_advanced_search:
        search_criteria['sub_county'] = int(sub_county_filter)

    ward_filter = str(
        request.GET.get('ward', '') if request.method == 'GET' else request.POST.get('ward', ''))
    if ward_filter != '':
        search_criteria['ward'] = int(ward_filter)

    doe_start_filter = str(
        request.GET.get('doe_start_filter', '') if request.method == 'GET' else request.POST.get('doe_start_filter',
                                                                                                 ''))

    start_date = request.GET.get('doe_start_filter',
                                 '') if request.method == 'GET' else request.POST.get(
        'doe_start_filter', '')

    if doe_start_filter != '' and is_advanced_search:
        search_criteria['enrolment_start_date'] = get_start_date(start_date)

    end_date_filter_original = request.GET.get('doe_end_filter',
                                               dt.today()) if request.method == 'GET' else request.POST.get(
        'doe_end_filter', dt.today())

    if end_date_filter_original != '' and is_advanced_search:
        search_criteria['enrolment_end_date'] = end_date_filter_original

    return search_criteria


def get_start_date(start_date):
    return '2015-10-01' if start_date == '' else start_date


def follow_ups(request):
    if request.user is not None and request.user.is_authenticated() and request.user.is_active:
        client_id = request.GET.get('client_id', '') if request.method == 'GET' else request.POST.get('client_id', '')
        if client_id is not None and client_id != 0:
            try:
                client = Client.objects.get(id=client_id)
                client_follow_ups = ClientFollowUp.objects.filter(client=client)

                follow_up_service_layer = FollowUpsServiceLayer(request.user, client)
                follow_up_perms = {
                    'can_create_follow_up': follow_up_service_layer.can_create_followup(),
                    'can_delete_follow_up': follow_up_service_layer.can_delete_followup(),
                    'can_edit_follow_up': follow_up_service_layer.can_edit_followup(),
                    'can_view_follow_up': follow_up_service_layer.can_view_followup()
                }

                page = request.GET.get('page', 1)
                paginator = Paginator(client_follow_ups, 20)
                follow_up_types = ClientFollowUpType.objects.all()
                follow_up_result_types = ClientLTFUResultType.objects.all()

                try:
                    displayed_follow_ups = paginator.page(page)
                except PageNotAnInteger:
                    displayed_follow_ups = paginator.page(1)
                except EmptyPage:
                    displayed_follow_ups = paginator.page(paginator.num_pages)
                current_user_belongs_to_same_ip_as_client = client.current_user_belongs_to_same_ip_as_client(
                    request.user.implementingpartneruser.implementing_partner_id)
                return render(request, 'client_follow_ups.html', {
                    'page': 'Follow Ups',
                    'page_title': 'Client Follow Ups Page',
                    'client': client,
                    'user': request.user,
                    'follow_up_perms': follow_up_perms,
                    'follow_ups': displayed_follow_ups,
                    'follow_up_types': follow_up_types,
                    'follow_up_result_types': follow_up_result_types,
                    'current_user_belongs_to_same_ip_as_client': current_user_belongs_to_same_ip_as_client or request.user.is_superuser
                })
            except Client.DoesNotExist:
                response_data = {
                    'status': 'failed',
                    'message': 'Operation not allowed. Client does not exist',
                    'client_id': client.id
                }
                return JsonResponse(json.dumps(response_data), safe=False)
            except Exception as e:
                return render(request, 'login.html')
    else:
        raise PermissionDenied


def client_profile(request):
    """ Returns client profile """
    user = request.user
    if user is not None and user.is_authenticated() and user.is_active:
        client_id = request.GET.get('client_id', '') if request.method == 'GET' else request.POST.get(
            'client_id', '')
        search_client_term = request.GET.get('search_client_term', '') if request.method == 'GET' else request.POST.get(
            'search_client_term', '')
        ip = None
        if client_id is not None and client_id != 0:
            try:
                ip = user.implementingpartneruser.implementing_partner
                ip_code = ip.code if ip else None
                if ip:
                    ip_code = ip.code
                else:
                    ip_code = None
            except Exception as e:
                ip_code = None

            client_found = None
            is_editable_by_ip = False
            can_add_intervention = False
            client_status = None

            if not ip:
                raise Exception("You do not belong to an implementing partner")

            ip_user_id = ip.id

            try:
                client_found = Client.objects.get(id=client_id)
                is_editable_by_ip = client_found.is_editable_by_ip(ip)
                can_add_intervention = client_found.can_add_intervention(ip)
                client_status = client_found.get_client_status(ip)

                if client_found is not None:
                    # get cash transfer details
                    cash_transfer_details = ClientCashTransferDetails.objects.get(client=client_found)
                    # create cash transfer details form
                    cash_transfer_details_form = ClientCashTransferDetailsForm(instance=cash_transfer_details,
                                                                               current_AGYW=client_found)
                    cash_transfer_details_form.save(commit=False)

                current_user_belongs_to_same_ip_as_client = client_found.current_user_belongs_to_same_ip_as_client(
                    ip_user_id)
                # intervention_action_permissions = InterventionActionPermissions(model=Intervention, user=request.user)
                return render(request, 'client_profile.html', {'page': 'clients',
                                                               'page_title': 'DREAMS Client Service Uptake',
                                                               'client': client_found,
                                                               'ct_form': cash_transfer_details_form,
                                                               'ct_id': cash_transfer_details.id,
                                                               'search_client_term': search_client_term,
                                                               'user': request.user,
                                                               'transfer_form': ClientTransferForm(ip_code=ip_code,
                                                                                                   initial={
                                                                                                       'client':
                                                                                                           client_found}),
                                                               'is_editable_by_ip': is_editable_by_ip,
                                                               'can_add_intervention': can_add_intervention,
                                                               'client_status': client_status,
                                                               '60_days_from_now': dt.now() + + timedelta(days=60),
                                                               'intervention_categories': InterventionCategory.objects.all(),
                                                               'current_user_belongs_to_same_ip_as_client': current_user_belongs_to_same_ip_as_client or user.is_superuser
                                                               })
            except ClientCashTransferDetails.DoesNotExist:
                cash_transfer_details_form = ClientCashTransferDetailsForm(current_AGYW=client_found)
                current_user_belongs_to_same_ip_as_client = client_found.current_user_belongs_to_same_ip_as_client(
                    ip_user_id)
                client_action_permissions = ClientActionPermissions(model=Client, user=user,
                                                                    enrolment=client_found)
                # intervention_action_permissions = InterventionActionPermissions(model=Intervention, user=request.user)
                # delegated_intervention_type_codes = get_delegated_intervention_type_codes(
                #     client_found.implementing_partner, request.user.implementingpartneruser.implementing_partner)

                return render(request, 'client_profile.html',
                              {'page': 'clients',
                               'page_title': 'DREAMS Client Service Uptake',
                               'client': client_found,
                               'ct_form': cash_transfer_details_form,
                               'search_client_term': search_client_term,
                               'user': request.user,
                               'transfer_form': ClientTransferForm(ip_code=ip_code, initial={'client': client_found}),
                               'is_editable_by_ip': is_editable_by_ip,
                               'can_add_intervention': can_add_intervention,
                               'client_status': client_status,
                               '60_days_from_now': dt.now() + + timedelta(days=60),
                               'intervention_categories': InterventionCategory.objects.all(),
                               'current_user_belongs_to_same_ip_as_client': current_user_belongs_to_same_ip_as_client or user.is_superuser,
                               'client_action_permissions': client_action_permissions
                               # 'intervention_action_permissions': intervention_action_permissions,
                               # 'delegated_intervention_type_codes': delegated_intervention_type_codes
                               })
            except Client.DoesNotExist:
                return render(request, 'login.html')
            except Exception as e:
                return render(request, 'login.html')
    else:
        raise PermissionDenied


"""
def get_delegated_intervention_type_codes(delegating_ip, delegated_ip):
    if delegated_ip == delegating_ip:
        return []

    delegations = ServiceDelegation.objects.filter(main_implementing_partner=delegating_ip,
                                                   delegated_implementing_partner=delegated_ip,
                                                   end_date__gt=datetime.now().date())
    delegations = list(delegations.values_list('intervention_type__code', flat=True))
    return delegations
"""


class ClientCreateView(CreateView):
    form_class = DemographicsForm

    def form_valid(self, form):
        try:
            user = self.request.user
            if user is not None and user.is_authenticated() and user.is_active:
                if self.request.method == 'GET':
                    return render(self.request, 'enrollment.html', {'client': None})
                elif self.request.method == 'POST' and self.request.is_ajax():
                    # process saving user
                    try:
                        ip_code = user.implementingpartneruser.implementing_partner.code
                    except Exception as e:
                        response_data = {
                            'status': 'fail',
                            'message': 'Enrollment Failed. You do not belong to an implementing partner',
                            'client_id': None,
                            'can_manage_client': user.has_perm('auth.can_manage_client'),
                            'can_change_client': user.has_perm('auth.can_change_client'),
                            'can_delete_client': user.has_perm('auth.can_delete_client')
                        }
                        return JsonResponse(json.dumps(response_data), safe=False)

                    client_enrolment_service_layer = ClientEnrolmentServiceLayer(self.request.user)

                    if not client_enrolment_service_layer.is_within_enrolment_dates(
                            form.cleaned_data['date_of_birth'], form.cleaned_data['date_of_enrollment']):
                        min_max_age = client_enrolment_service_layer.get_minimum_maximum_enrolment_age(
                            client_enrolment_service_layer.ENROLMENT_CUTOFF_DATE)

                        response_data = {
                            'status': 'fail',
                            'message': "The client is not within the accepted age range. At the date of enrolment the "
                                       "age of the client must be between " + str(
                                min_max_age[0]) + " and " + str(min_max_age[1] + " years."),
                            'client_id': None,
                            'can_manage_client': user.has_perm('auth.can_manage_client'),
                            'can_change_client': user.has_perm('auth.can_change_client'),
                            'can_delete_client': user.has_perm('auth.can_delete_client')
                        }
                        return JsonResponse(json.dumps(response_data), safe=False)

                    client = form.save()

                    # Generate client dreams_id
                    cursor = db_conn_2.cursor()
                    try:
                        cursor.execute(
                            """
                            SELECT (max(CONVERT(SUBSTRING_INDEX(dreams_id, '/', -1), UNSIGNED INTEGER )) + 1)
                            from DreamsApp_client WHERE dreams_id is not null and ward_id is not null
                            AND dreams_id REGEXP CONCAT('^', CAST(%s as decimal(4, 0)), '/', CAST(%s as decimal(4, 0)),'/')
                            ;""",
                            (ip_code, client.ward.code))
                        next_serial = cursor.fetchone()[0]
                        if next_serial is None:
                            next_serial = 1

                        client.dreams_id = str(ip_code) + '/' + str(client.ward.code if client.ward != None else '') \
                                           + '/' + str(next_serial)

                    except Exception as e:
                        next_serial = 1
                        client.dreams_id = str(ip_code) + '/' + str(1) \
                                           + '/' + str(next_serial)
                    finally:
                        cursor.close()
                        client.save(update_fields=['dreams_id'])

                    if self.request.is_ajax():
                        response_data = {
                            'status': 'success',
                            'message': 'Enrollment to DREAMS successful. Redirecting you to the full enrolment data '
                                       'view',
                            'client_id': client.id,
                            'can_manage_client': user.has_perm('auth.can_manage_client'),
                            'can_change_client': user.has_perm('auth.can_change_client'),
                            'can_delete_client': user.has_perm('auth.can_delete_client')
                        }
                        return JsonResponse(json.dumps(response_data), safe=False)
                    else:
                        # redirect to page
                        return redirect('clients')
            else:
                raise PermissionDenied

        except Exception as e:
            response_data = {
                'status': 'fail',
                'message': str(e),
                'client_id': None,
                'can_manage_client': user.has_perm('auth.can_manage_client'),
                'can_change_client': user.has_perm('auth.can_change_client'),
                'can_delete_client': user.has_perm('auth.can_delete_client')
            }
            return JsonResponse(json.dumps(response_data), safe=False)

    def form_invalid(self, form):
        user = self.request.user
        response_data = {
            'status': 'fail',
            'message': form.errors,
            'client_id': None,
            'can_manage_client': user.has_perm('auth.can_manage_client'),
            'can_change_client': user.has_perm('auth.can_change_client'),
            'can_delete_client': user.has_perm('auth.can_delete_client')
        }
        return JsonResponse(json.dumps(response_data), safe=False)


## NOT USED IN APPLICATION
class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'

    def get_object(self, queryset=None):
        try:
            if self.request.method == 'GET':
                client_id = int(self.request.GET['client_id'])
                client = Client.objects.defer('date_of_enrollment', 'date_of_birth').get(id__exact=client_id)

            elif self.request.method == 'POST':
                client_id = int(str(self.request.POST.get('client_id')))
                client = Client.objects.get(id=client_id, voided=False)

            self.object = client
            return self.object
        except AttributeError:
            return None

    def form_valid(self, form):
        try:
            user = self.request.user
            if user is not None and user.is_authenticated() and user.is_active:  # and request.user.is_superuser:
                client = self.object

                if self.request.method == 'GET':
                    if client is None:
                        redirect('clients')
                    if self.request.is_ajax():
                        response_data = {'client': serializers.serialize('json', [client, ])}
                        return JsonResponse(response_data, safe=False)
                    else:
                        # redirect to page
                        return render(self.request, 'enrollment.html', {'client': client})
                    return redirect('clients')

                elif self.request.method == 'POST':
                    ip = None
                    try:
                        ip = user.implementingpartneruser.implementing_partner
                    except Exception as e:
                        if not ip:
                            response_data = {
                                'status': 'failed',
                                'message': 'You do not belong to any implementing partner',
                                'client_id': client.id
                            }
                            return JsonResponse(json.dumps(response_data), safe=False)

                    if not client.is_editable_by_ip(ip) or client.exited:
                        response_data = {
                            'status': 'failed',
                            'message': 'Operation not allowed. Client is not editable by your Implementing partner or is exited',
                            'client_id': client.id
                        }
                        return JsonResponse(json.dumps(response_data), safe=False)

                    if client.implementing_partner != ip:
                        # user and client IPs dont match. Return error message
                        response_data = {
                            'status': 'failed',
                            'message': 'Operation not allowed. Client is not enrolled by your Implementing partner',
                            'client_id': client.id
                        }
                        return JsonResponse(json.dumps(response_data), safe=False)

                    client_enrolment_service_layer = ClientEnrolmentServiceLayer(user)
                    date_of_birth = datetime.strptime(self.request.POST.get('date_of_birth'), '%Y-%m-%d').date()
                    date_of_enrollment = datetime.strptime(self.request.POST.get('date_of_enrollment'),
                                                           '%Y-%m-%d').date()

                    if not client_enrolment_service_layer.is_within_enrolment_dates(date_of_birth, date_of_enrollment):
                        min_max_age = client_enrolment_service_layer.get_minimum_maximum_enrolment_age(
                            client_enrolment_service_layer.ENROLMENT_CUTOFF_DATE)

                        response_data = {
                            'status': 'failed',
                            'message': "The client is not within the accepted age range. At the date of enrolment the age of the client must be between " + str(
                                min_max_age[0]) + " and " + str(min_max_age[1] + " years."),
                            'client_id': client.id
                        }
                        return JsonResponse(json.dumps(response_data), safe=False)

                    # process editing user
                    client.implementing_partner = ImplementingPartner.objects.filter(
                        code__exact=str(self.request.POST.get('implementing_partner', ''))).first()
                    client.first_name = str(self.request.POST.get('first_name', ''))
                    client.middle_name = str(self.request.POST.get('middle_name', ''))
                    client.last_name = str(self.request.POST.get('last_name', ''))
                    client.date_of_birth = str(date_of_birth)
                    client.is_date_of_birth_estimated = bool(str(self.request.POST.get('is_date_of_birth_estimated')))
                    client.verification_document = VerificationDocument.objects.filter(
                        code__exact=str(self.request.POST.get('verification_document', ''))).first()
                    client.verification_doc_no = str(self.request.POST.get('verification_doc_no', ''))
                    client.date_of_enrollment = str(
                        datetime.strptime(self.request.POST.get('date_of_enrollment', dt.now()), '%Y-%m-%d').date())
                    client.age_at_enrollment = int(str(self.request.POST.get('age_at_enrollment')))
                    client.marital_status = MaritalStatus.objects.filter(
                        code__exact=str(self.request.POST.get('marital_status', ''))).first()
                    client.phone_number = str(self.request.POST.get('phone_number', ''))
                    client.dss_id_number = str(self.request.POST.get('dss_id_number', ''))
                    client.county_of_residence = County.objects.filter(
                        code__exact=self.request.POST.get('county_of_residence', '')).first()
                    client.sub_county = SubCounty.objects.filter(
                        code__exact=self.request.POST.get('sub_county', '')).first()
                    client.ward = Ward.objects.filter(code__exact=self.request.POST.get('ward', 0)).first()
                    client.informal_settlement = str(self.request.POST.get('informal_settlement', ''))
                    client.village = str(self.request.POST.get('village', ''))
                    client.landmark = str(self.request.POST.get('landmark', ''))
                    client.dreams_id = str(self.request.POST.get('dreams_id', ''))
                    client.guardian_name = str(self.request.POST.get('guardian_name', ''))
                    client.relationship_with_guardian = str(self.request.POST.get('relationship_with_guardian', ''))
                    client.guardian_phone_number = str(self.request.POST.get('guardian_phone_number', ''))
                    client.guardian_national_id = str(self.request.POST.get('guardian_national_id', ''))
                    client.save(user_id=self.request.user.id, action="UPDATE")
                    if self.request.is_ajax():
                        response_data = {
                            'status': 'success',
                            'message': 'Client Details Updated successfuly.',
                            'client_id': client.id,
                            'can_manage_client': self.request.user.has_perm('auth.can_manage_client'),
                            'can_change_client': self.request.user.has_perm('auth.can_change_client'),
                            'can_delete_client': self.request.user.has_perm('auth.can_delete_client')
                        }
                        return JsonResponse(json.dumps(response_data), safe=False)
                    else:
                        # redirect to page
                        return redirect('clients')

            else:
                raise PermissionDenied
        except Exception as e:
            tb = traceback.format_exc(e)
            return HttpResponseServerError(tb)

    def form_invalid(self, form):
        response_data = {
            'status': 'failed',
            'message': 'There are errors'
        }
        return JsonResponse(json.dumps(response_data), safe=False)


## NOT USED IN APPLICATION
class ClientDeleteView(DeleteView):
    model = Client

    def get_object(self, queryset=None):
        try:
            if self.request.method == 'GET' and self.request.is_ajax():
                client_id = int(self.request.GET['client_id'])
                self.object = Client.objects.get(id__exact=client_id)
            else:
                self.object = None
            return self.object
        except AttributeError:
            return None

    def form_valid(self, form):
        try:
            user = self.request.user
            if user is None or not user.is_authenticated() or not user.is_active:
                raise PermissionDenied

            if self.request.method == 'POST' or not self.request.is_ajax():
                raise PermissionDenied

            client = self.object
            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'failed',
                        'message': 'You do not belong to any implementing partner',
                        'client_id': client.id
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

            if not client.is_editable_by_ip(ip) or client.exited:
                response_data = {
                    'status': 'failed',
                    'message': 'Operation not allowed. Client is not editable by your Implementing partner or is exited',
                    'client_id': client.id
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            # check if client and user IPs match
            if client.implementing_partner != ip:
                response_data = {
                    'status': 'failed',
                    'message': 'Operation not allowed. Client is not enrolled by your Implementing partner',
                    'client_id': client.id
                }
                return JsonResponse(json.dumps(response_data), safe=False)

            # check if client has interventions
            if Intervention.objects.filter(client=client).count() > 0:
                # Upating audit log
                log_custom_actions(self.request.user.id, "DreamsApp_client", client.id, "DELETE", 'FAILED')
                response_data = {
                    'status': 'fail',
                    'message': 'This client cannot be deleted because they have interventions.'
                }
            else:
                client.delete()
                # Upating audit log
                log_custom_actions(self.request.user.id, "DreamsApp_client", client.id, "DELETE", 'SUCCESS')
                response_data = {
                    'status': 'success',
                    'message': 'Client Details Deleted successfuly.'
                }
            return JsonResponse(json.dumps(response_data), safe=False)

        except Exception as e:
            tb = traceback.format_exc(e)
            return HttpResponseServerError(tb)

    def form_invalid(self, form):
        response_data = {
            'status': 'failed',
            'message': 'There are errors'
        }
        return JsonResponse(json.dumps(response_data), safe=False)


class ClientDemographicsCreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    form_class = DemographicsForm

    def get_object(self, queryset=None):
        try:
            if not self.request.is_ajax():
                raise PermissionDenied
            if self.request.method != 'POST':
                raise PermissionDenied

            client_id = self.request.POST['client']
            if client_id is not None and client_id != "0":
                return Client.objects.get(id=client_id)
            else:
                return None
        except Exception as e:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ClientDemographicsCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ClientDemographicsCreateUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            client_enrolment_service_layer = ClientEnrolmentServiceLayer(self.request.user)
            if not client_enrolment_service_layer.is_within_enrolment_dates(form.instance.date_of_birth,
                                                                            form.instance.date_of_enrollment):
                min_max_age = client_enrolment_service_layer.get_minimum_maximum_enrolment_age(
                    client_enrolment_service_layer.ENROLMENT_CUTOFF_DATE)

                response_data = {
                    'status': 'fail',
                    'errors': [
                        "The client is not within the accepted age range. At the date of enrolment the age of the client"
                        " must be between " + str(
                            min_max_age[0]) + " and " + str(min_max_age[1] + " years.")],
                    'client_age': self.object.get_current_age()
                }
                return JsonResponse(response_data, status=500)

            client = form.save(commit=False)
            client.implementing_partner = ImplementingPartner.objects.get(id=form.initial["implementing_partner"])
            client.dreams_id = form.initial["dreams_id"]
            client.save()

            response_data = {
                'status': 'success',
                'errors': form.errors,
                'client_age': self.object.get_current_age()
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            response_data = {
                'status': 'fail',
                'errors': str(e)
            }
            return JsonResponse(response_data, status=500)

    def form_invalid(self, form):
        response_data = {
            'status': 'fail',
            'errors': form.errors
        }
        return JsonResponse(response_data, status=500)


class IndividualHouseHoldCreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    form_class = IndividualAndHouseholdForm

    def get_object(self, queryset=None):
        try:
            if not self.request.is_ajax():
                raise PermissionDenied
            if self.request.method != 'POST':
                raise PermissionDenied

            client_id = self.request.POST['client']
            if client_id is not None and client_id != "0":
                client = Client.objects.get(id=int(client_id), voided=False)
                individialhousehold_queryset = client.clientindividualandhouseholddata_set
                individialhousehold = individialhousehold_queryset.get() if individialhousehold_queryset.exists() else None
                return individialhousehold
            else:
                return None
        except Exception as e:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(IndividualHouseHoldCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(IndividualHouseHoldCreateUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        response_data = {
            'status': 'success'
        }
        return JsonResponse(response_data, status=200)

    def form_invalid(self, form):
        response_data = {
            'status': 'fail',
            'errors': form.errors
        }
        return JsonResponse(response_data, status=500)


class EducationAndEmploymentCreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    form_class = EducationAndEmploymentForm

    def get_object(self, queryset=None):
        try:
            if not self.request.is_ajax():
                raise PermissionDenied
            if self.request.method != 'POST':
                raise PermissionDenied

            client_id = self.request.POST['client']
            if client_id is not None and client_id != "0":
                client = Client.objects.get(id=int(client_id), voided=False)
                educationandemployment_queryset = client.clienteducationandemploymentdata_set
                educationandemployment = educationandemployment_queryset.get() if educationandemployment_queryset.exists() else None
                return educationandemployment
            else:
                return None
        except Exception as e:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EducationAndEmploymentCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EducationAndEmploymentCreateUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        response_data = {
            'status': 'success'
        }
        return JsonResponse(response_data, status=200)

    def form_invalid(self, form):
        response_data = {
            'status': 'fail',
            'errors': form.errors
        }
        return JsonResponse(response_data, status=500)


class HIVTestingCreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    form_class = HivTestForm

    def get_object(self, queryset=None):
        try:
            if not self.request.is_ajax():
                raise PermissionDenied
            if self.request.method != 'POST':
                raise PermissionDenied

            client_id = self.request.POST['client']
            if client_id is not None and client_id != "0":
                client = Client.objects.get(id=int(client_id), voided=False)
                clienthivtesting_queryset = client.clienthivtestingdata_set
                clienthivtesting = clienthivtesting_queryset.get() if clienthivtesting_queryset.exists() else None
                return clienthivtesting
            else:
                return None
        except Exception as e:
            raise ValueError

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(HIVTestingCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(HIVTestingCreateUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        response_data = {
            'status': 'success'
        }
        return JsonResponse(response_data, status=200)

    def form_invalid(self, form):
        response_data = {
            'status': 'fail',
            'errors': form.errors
        }
        return JsonResponse(response_data, status=500)


class SexualityCreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    form_class = SexualityForm

    def get_object(self, queryset=None):
        try:
            if not self.request.is_ajax():
                raise PermissionDenied
            if self.request.method != 'POST':
                raise PermissionDenied

            client_id = self.request.POST['client']
            if client_id is not None and client_id != "0":
                client = Client.objects.get(id=int(client_id), voided=False)
                sexualactivity_queryset = client.clientsexualactivitydata_set
                sexualactivity = sexualactivity_queryset.get() if sexualactivity_queryset.exists() else None
                return sexualactivity
            else:
                return None
        except Exception as e:
            raise ValueError

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SexualityCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SexualityCreateUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        response_data = {
            'status': 'success'
        }
        return JsonResponse(response_data, status=200)

    def form_invalid(self, form):
        response_data = {
            'status': 'fail',
            'errors': form.errors
        }
        return JsonResponse(response_data, status=500)


class ReproductiveHealthCreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    form_class = ReproductiveHealthForm

    def get_object(self, queryset=None):
        try:
            if not self.request.is_ajax():
                raise PermissionDenied
            if self.request.method != 'POST':
                raise PermissionDenied

            client_id = self.request.POST['client']
            if client_id is not None and client_id != "0":
                client = Client.objects.get(id=int(client_id), voided=False)
                reproductivehealth_queryset = client.clientreproductivehealthdata_set
                reproductivehealth = reproductivehealth_queryset.get() if reproductivehealth_queryset.exists() else None
                return reproductivehealth
            else:
                return None
        except Exception as e:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ReproductiveHealthCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ReproductiveHealthCreateUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        response_data = {
            'status': 'success'
        }
        return JsonResponse(response_data, status=200)

    def form_invalid(self, form):
        response_data = {
            'status': 'fail',
            'errors': form.errors
        }
        return JsonResponse(response_data, status=500)


class GenderBasedViolenceCreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    form_class = GBVForm

    def get_object(self, queryset=None):
        try:
            if not self.request.is_ajax():
                raise PermissionDenied
            if self.request.method != 'POST':
                raise PermissionDenied

            client_id = self.request.POST['client']
            if client_id is not None and client_id != "0":
                client = Client.objects.get(id=int(client_id), voided=False)
                gbv_queryset = client.clientgenderbasedviolencedata_set
                gbv = gbv_queryset.get() if gbv_queryset.exists() else None
                return gbv
            else:
                return None
        except Exception as e:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(GenderBasedViolenceCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(GenderBasedViolenceCreateUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        response_data = {
            'status': 'success'
        }
        return JsonResponse(response_data, status=200)

    def form_invalid(self, form):
        response_data = {
            'status': 'fail',
            'errors': form.errors
        }
        return JsonResponse(response_data, status=500)


class DrugUseCreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    form_class = DrugUseForm

    def get_object(self, queryset=None):
        try:
            if not self.request.is_ajax():
                raise PermissionDenied
            if self.request.method != 'POST':
                raise PermissionDenied

            client_id = self.request.POST['client']
            if client_id is not None and client_id != "0":
                client = Client.objects.get(id=int(client_id), voided=False)
                druguse_queryset = client.clientdrugusedata_set
                druguse = druguse_queryset.get() if druguse_queryset.exists() else None
                return druguse
            else:
                return None
        except Exception as e:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DrugUseCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DrugUseCreateUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        response_data = {
            'status': 'success'
        }
        return JsonResponse(response_data, status=200)

    def form_invalid(self, form):
        response_data = {
            'status': 'fail',
            'errors': form.errors
        }
        return JsonResponse(response_data, status=500)


class ProgramParticipationCreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    form_class = DreamsProgramParticipationForm

    def get_object(self, queryset=None):
        try:
            if not self.request.is_ajax():
                raise PermissionDenied
            if self.request.method != 'POST':
                raise PermissionDenied

            client_id = self.request.POST['client']
            if client_id is not None and client_id != "0":
                client = Client.objects.get(id=int(client_id), voided=False)
                programparticipation_queryset = client.clientparticipationindreams_set
                programparticipation = programparticipation_queryset.get() if programparticipation_queryset.exists() else None
                return programparticipation
            else:
                return None
        except Exception as e:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProgramParticipationCreateUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProgramParticipationCreateUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        response_data = {
            'status': 'success'
        }
        return JsonResponse(response_data, status=200)

    def form_invalid(self, form):
        response_data = {
            'status': 'fail',
            'errors': form.errors
        }
        return JsonResponse(response_data, status=500)


def get_client_status(client):
    status = ''
    try:
        if client.voided:
            status += ' Voided'
        if client.exited:
            if status != '':
                status += ' & '
            status += 'Exited'
        if status != '':
            status = status[:0] + '( ' + status[0:]
            last_index = len(status)
            status = status[:last_index] + ' ) ' + status[last_index:]
        return status
    except Exception as e:
        return 'Invalid Status'


def is_not_null_or_empty(str):
    return str is not None and str is not ""


def unexit_client(request):
    if request.user is not None and request.user.is_authenticated() and request.user.is_active and request.user.has_perm(
            'DreamsApp.can_exit_client'):
        try:
            client_id = int(str(request.POST.get('client_id', '0')))
            reason_for_exit = str(request.POST.get('reason_for_unexit', ''))
            date_of_exit = request.POST.get('date_of_unexit', datetime.now())
            client = Client.objects.get(id=client_id)
            try:
                if not (client.current_user_belongs_to_same_ip_as_client(
                        request.user.implementingpartneruser.implementing_partner_id) or request.user.is_superuser):
                    raise PermissionDenied
            except:
                response_data = {
                    'status': 'failed',
                    'message': 'Permission denied. You must belong to the same IP as the client to be able to update it.'
                }
                return JsonResponse(response_data, status=500)

            if dt.strptime(str(date_of_exit), '%Y-%m-%d').date() > dt.now().date():
                response_data = {
                    'status': 'fail',
                    'message': 'Selected unexit date cannot be later than today.'
                }
                return JsonResponse(response_data)

            if dt.strptime(str(date_of_exit), '%Y-%m-%d').date() < client.date_of_enrollment:
                response_data = {
                    'status': 'fail',
                    'message': 'Selected unexit date cannot be earlier than client enrolment date.'
                }
                return JsonResponse(response_data)

            client.exited = not client.exited
            client.reason_exited = reason_for_exit
            client.exited_by = request.user
            client.date_exited = make_aware(
                dt.combine(dt.strptime(date_of_exit, "%Y-%m-%d").date(), datetime.now().time()), timezone=timezone.utc,
                is_dst=None)
            client.save()
            response_data = {
                'status': 'success',
                'message': 'Client Exit Undone',
                'client_id': client.id,
                'client_status': get_client_status(client)
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            response_data = {
                'status': 'failed',
                'message': 'Invalid client Id: ' + str(e)
            }
            return JsonResponse(response_data, status=500)
    else:
        response_data = {
            'status': 'failed',
            'message': 'Permission Denied. Please contact System Administrator for help.'
        }
        return JsonResponse(response_data, status=500)


def exit_client(request):
    OTHER_CODE = 6

    if request.user is not None and request.user.is_authenticated() and request.user.is_active and request.user.has_perm(
            'DreamsApp.can_exit_client'):
        try:
            client_id = int(str(request.POST.get('client_id')))
            reason_for_exit = ExitReason.objects.get(id__exact=int(request.POST.get('reason_for_exit', '')))
            date_of_exit = request.POST.get('date_of_exit', datetime.now())
            exit_comment = request.POST.get('exit_comment')

            client = Client.objects.get(id=client_id)
            if not client:
                response_data = {
                    'status': 'failed',
                    'message': 'There is no client found.'
                }
                return JsonResponse(response_data, status=500)

            try:
                if not (client.current_user_belongs_to_same_ip_as_client(
                        request.user.implementingpartneruser.implementing_partner_id) or request.user.is_superuser):
                    raise PermissionDenied
            except:
                response_data = {
                    'status': 'failed',
                    'message': 'Permission denied. You must belong to the same IP as the client to be able to update it.'
                }
                return JsonResponse(response_data, status=500)

            last_intervention_offered = get_last_intervention_offered(client)

            if last_intervention_offered and dt.strptime(str(last_intervention_offered.intervention_date),
                                                         '%Y-%m-%d').date() > dt.strptime(date_of_exit,
                                                                                          '%Y-%m-%d').date():
                response_data = {
                    'status': 'failed',
                    'message': 'You cannot exit this client since she has received an intervention after the selected exit date.'
                }
                return JsonResponse(response_data, status=500)

            if dt.strptime(str(date_of_exit), '%Y-%m-%d').date() > dt.now().date():
                response_data = {
                    'status': 'fail',
                    'message': 'Selected exit date cannot be later than today.'
                }
                return JsonResponse(response_data)

            if dt.strptime(str(date_of_exit), '%Y-%m-%d').date() < client.date_of_enrollment:
                response_data = {
                    'status': 'fail',
                    'message': 'Selected exit date cannot be earlier than client enrolment date.'
                }
                return JsonResponse(response_data)

            if reason_for_exit is not None:
                if reason_for_exit.code == OTHER_CODE:
                    if is_not_null_or_empty(exit_comment):
                        exited_client = other_client_exit(client, reason_for_exit, exit_comment, request.user,
                                                          date_of_exit)
                    else:
                        raise Exception('Reason for exit missing')
                else:
                    exited_client = client_exit(client, reason_for_exit, request.user, date_of_exit)

            response_data = {
                'status': 'success',
                'message': 'Client Exited',
                'client_id': exited_client.id,
                'client_status': get_client_status(exited_client)
            }
            return JsonResponse(response_data, status=200)
        except Exception as e:
            response_data = {
                'status': 'failed',
                'message': 'Invalid client Id: ' + str(e)
            }
            return JsonResponse(response_data, status=500)
    else:
        response_data = {
            'status': 'failed',
            'message': 'Permission Denied. Please contact System Administrator for help.'
        }
        return JsonResponse(response_data, status=500)


def other_client_exit(client, reason_for_exit, exit_comment, exit_user, date_of_exit):
    client.exited = True
    client.exit_reason = reason_for_exit
    client.reason_exited = exit_comment
    client.exited_by = exit_user
    client.date_exited = make_aware(dt.combine(dt.strptime(date_of_exit, "%Y-%m-%d").date(), datetime.now().time()),
                                    timezone=timezone.utc, is_dst=None)
    client.save()
    return client


def client_exit(client, reason_for_exit, exit_user, date_of_exit):
    client.exited = True
    client.exit_reason = reason_for_exit
    client.exited_by = exit_user
    client.date_exited = make_aware(dt.combine(dt.strptime(date_of_exit, "%Y-%m-%d").date(), datetime.now().time()),
                                    timezone=timezone.utc, is_dst=None)
    client.save()
    return client


def get_last_intervention_offered(client: Client):
    last_intervention = None
    get_last_intervention = Intervention.objects.filter(client=client).order_by("-intervention_date")
    if get_last_intervention:
        last_intervention = get_last_intervention.first()
    return last_intervention


def testajax(request):
    return render(request, 'testAjax.html')


# Use /ivgetTypes/ in the post url to access the method
# Handles post request for intervention types.
# Receives category_code from request and searches for types in the database

def get_external_organisation(request):
    try:
        if request.method == 'GET' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
            response_data = {}
            external_orgs = serializers.serialize('json', ExternalOrganisation.objects.all())
            response_data["external_orgs"] = external_orgs
            return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def get_unsuccessful_followup_attempts(request):
    try:
        if is_valid_get_request(request):
            response_data = {}
            client_id = int(request.GET.get('current_client_id'))
            client = Client.objects.get(id=client_id)
            unsuccessful_follow_up_attempts = ClientFollowUp.objects.filter(client=client,
                                                                            result_of_followup=ClientLTFUResultType.objects.filter(
                                                                                name='Lost').first()).all()
            response_data['unsuccessful_follow_up_attempts'] = len(unsuccessful_follow_up_attempts)
            return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def get_exit_reasons(request):
    try:
        if is_valid_get_request(request):
            response_data = {}
            exit_reasons = serializers.serialize('json', ExitReason.objects.all())
            response_data["exit_reasons"] = exit_reasons
            return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def is_valid_get_request(request):
    return request.method == 'GET' and request.user is not None and request.user.is_authenticated() and request.user.is_active


def is_valid_post_request(request):
    return request.method == 'POST' and request.user is not None and request.user.is_authenticated() and request.user.is_active


def get_intervention_types(request):
    try:
        if request.method == 'POST' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
            response_data = {}
            category_code = request.POST.get('category_code')
            current_client_id = request.POST.get('current_client_id', 0)
            # get current client
            current_client = Client.objects.get(id=current_client_id)
            if current_client is None:
                raise Exception
            # Get category by code and gets all related types
            # Returns an object with itypes property
            # given_intervention_type_ids = Intervention.objects.values_list('intervention_type', flat=True). \
            #     filter(client=current_client). \
            #     distinct()  # select distinct intervention type ids given to a user
            i_category = InterventionCategory.objects.get(code__exact=category_code)
            # compute age at enrollment
            current_age = current_client.get_current_age()
            i_types = InterventionType.objects.filter(intervention_category__exact=i_category.id, ) \
                .order_by('code')
            # .exclude(is_given_once=True, id__in=given_intervention_type_ids).order_by('code')
            """This code has been commented out to allow for change of intervention types for one time interventions"""
            # get id's of interventions that can only be given once and are already given
            i_types = serializers.serialize('json', i_types)
            response_data["itypes"] = i_types
            return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def get_intervention_type(request):
    try:
        if request.method == 'POST' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
            response_data = {}
            type_code = request.POST.get('type_code')
            i_type = serializers.serialize('json',
                                           InterventionType.objects.filter(code__exact=type_code).order_by('code'))
            # i_type = serializers.serialize('json',
            #                                InterventionType.objects.get(code=type_code))
            response_data["itype"] = i_type
            return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


# use /ivSave/ to post to the method
# Gets intervention_type_id,  from request
def save_intervention(request):
    try:
        user = request.user
        if is_valid_post_request(request) and user.has_perm('DreamsApp.add_intervention'):
            try:
                client_id = request.POST.get('client')
                client_key = 'client-{}'.format(client_id)
                client = cache.get(client_key)

                if not client:
                    client = Client.objects.get(id__exact=int(client_id))

                # if client.exited or client.voided:
                #     client = Client.objects.get(id__exact=int(client_id))

                cache_value(client_key, client)

                status = True
                if client.voided:
                    message = 'Error: You cannot Add Sevices to a voided Client. ' \
                              'Please contact System Administrator for help.'
                    status = False
                if client.exited:
                    message = 'Error: You cannot Add Sevices to a Client Exited from DREAMS. ' \
                              'Please contact System Administrator for help.'
                    status = False
                if not status:
                    response_data = {
                        'status': 'fail',
                        'message': message
                    }
                    return JsonResponse(response_data)
            except:
                response_data = {
                    'status': 'fail',
                    'message': "Error: Client with given ID Cannot be found. "
                               "Please contact System Administrator for help."
                }
                return JsonResponse(response_data)

            # Check if user belongs to an Ip
            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail',
                        'message': "You do not belong to any implementing partner"
                    }
                    return JsonResponse(response_data)

            if ip is not None:
                intervention_type_code = int(request.POST.get('intervention_type_code'))
                intervention_type_key = 'intervention-type-{}'.format(intervention_type_code)

                intervention_type = cache.get(intervention_type_key)
                if not intervention_type:
                    intervention_type = InterventionType.objects.get(code__exact=intervention_type_code)
                cache_value(intervention_type_key, intervention_type)

                """Check that this is not a one time intervention that has already been given to the client"""
                try:
                    """Get client intervention filtered by intervention types"""
                    intervention_key = '{}-{}'.format(client.id, intervention_type_code)
                    client_interventions_count = cache.get(intervention_key)

                    if client_interventions_count is None:
                        client_interventions_count = Intervention.objects.filter(intervention_type=intervention_type,
                                                                                 client=client).exclude(
                            voided=True).count()

                    cache_value(intervention_key, client_interventions_count)

                    if intervention_type.is_given_once and client_interventions_count > 0:
                        response_data = {
                            'status': 'fail',
                            'message': "Error: This is a one time service that has already been offered. Please "
                                       "consider editing if necessary "
                        }
                        return JsonResponse(response_data)
                except Exception as e:
                    raise Exception(str(e))

                intervention_date = dt.strptime(request.POST.get('intervention_date'), '%Y-%m-%d').date()

                # check if external organisation is selected
                external_organization_checkbox = request.POST.get('external_organization_checkbox')
                external_organization_code = request.POST.get('external_organization_code')
                other_external_organization_code = request.POST.get('other_external_organization_code')
                intervention_by_referral = request.POST.get('intervention_by_referral')
                referral_id = request.POST.get('referral_id')
                referral = None

                intervention_is_by_referral = True if intervention_by_referral == INTERVENTION_BY_REFERRAL else False
                if intervention_is_by_referral:
                    if external_organization_code:
                        if client.date_of_enrollment is not None and intervention_date < client.date_of_enrollment:
                            response_data = {
                                'status': 'fail',
                                'message': "Error: The intervention date must be after the client's enrollment date. "
                            }
                            return JsonResponse(response_data)

                    if not referral_id:
                        response_data = {
                            'status': 'fail',
                            'message': "Error: The intervention must have associated referral."
                        }
                        return JsonResponse(response_data)

                    referral = Referral.objects.get(pk=referral_id)
                    if referral.referral_expiration_date < dt.now().date():
                        response_data = {
                            'status': 'fail',
                            'message': "Error: This referral has already expired and cannot be completed."
                        }
                        return JsonResponse(response_data)

                    referral_service_layer = ReferralServiceLayer(request.user, referral)
                    if not referral_service_layer.can_complete_referral():
                        response_data = {
                            'status': 'fail',
                            'message': "Error: You do not have permission to complete this referral."
                        }
                        return JsonResponse(response_data)

                else:
                    if external_organization_checkbox:
                        if not external_organization_code:
                            response_data = {
                                'status': 'fail',
                                'message': "Error: External organisation must be selected if checkbox is checked."
                            }
                            return JsonResponse(response_data)
                    else:
                        if client.date_of_enrollment is not None and intervention_date < client.date_of_enrollment:
                            response_data = {
                                'status': 'fail',
                                'message': "Error: The intervention date must be after the client's enrollment date. "
                            }
                            return JsonResponse(response_data)

                if intervention_date > dt.now().date():
                    response_data = {
                        'status': 'fail',
                        'message': "Error: The intervention date must be before or on the current date. "
                    }
                    return JsonResponse(response_data)

                if intervention_type_code is not None and type(intervention_type_code) is int:
                    htsresult = HTSResult.objects.all()
                    pregnancytestresult = PregnancyTestResult.objects.all()

                    with transaction.atomic():
                        intervention = Intervention()
                        intervention.client = client
                        intervention.intervention_type = intervention_type
                        intervention.name_specified = intervention_type.name if not intervention_type.is_specified else request.POST.get(
                            'other_specify', '')
                        intervention.intervention_date = request.POST.get('intervention_date')
                        created_by = User.objects.get(id__exact=int(request.POST.get('created_by')))
                        intervention.created_by = created_by
                        intervention.changed_by = created_by
                        intervention.date_created = dt.now()
                        intervention.date_changed = dt.now()
                        intervention.comment = request.POST.get('comment', '')

                        if intervention_by_referral == INTERVENTION_BY_REFERRAL:
                            referral.referral_status = ReferralStatus.objects.get(code__exact=REFERRAL_COMPLETED_STATUS)
                            intervention.referral = referral

                            if external_organization_code:
                                intervention.external_organisation = ExternalOrganisation.objects.get(
                                    pk=external_organization_code)
                                intervention.implementing_partner = ImplementingPartner.objects. \
                                    get(id__exact=created_by.implementingpartneruser.implementing_partner.id)

                                if other_external_organization_code:
                                    intervention.external_organisation_other = other_external_organization_code
                            else:
                                intervention.implementing_partner = referral.referring_ip
                            referral.save()

                        else:
                            if external_organization_checkbox:
                                intervention.external_organisation = ExternalOrganisation.objects.get(
                                    pk=external_organization_code)
                                if other_external_organization_code:
                                    intervention.external_organisation_other = other_external_organization_code

                            intervention.implementing_partner = ImplementingPartner.objects. \
                                get(id__exact=created_by.implementingpartneruser.implementing_partner.id)

                        if intervention_type.has_hts_result:
                            if request.POST.get('hts_result'):
                                intervention.hts_result = htsresult.get(
                                    code__exact=int(request.POST.get('hts_result')))

                        if intervention_type.has_pregnancy_result:
                            if request.POST.get('pregnancy_test_result'):
                                intervention.pregnancy_test_result = pregnancytestresult.get(
                                    code__exact=int(request.POST.get('pregnancy_test_result')))

                        if intervention_type.has_ccc_number:
                            intervention.client_ccc_number = request.POST.get('client_ccc_number')

                        if intervention_type.has_no_of_sessions:
                            intervention.no_of_sessions_attended = request.POST.get('no_of_sessions_attended')

                        intervention.save(user_id=request.user.id, action="INSERT")  # Logging

                        intervention_type_category_cache_key = 'client-{}-intervention-type-category-{}'.format(
                            intervention.client.id, intervention.intervention_type.intervention_category.code)
                        cache.delete(intervention_type_category_cache_key)

                        if intervention_by_referral == INTERVENTION_BY_REFERRAL:
                            response_data = {
                                'status': 'success',
                                'message': 'Referral successfully completed'
                            }
                            return JsonResponse(response_data)

                        else:
                            # using defer() miraculously solved serialization problem of datetime properties.
                            # intervention = Intervention.objects.defer('date_changed', 'intervention_date',
                            #                                           'date_created'). \
                            #     get(id__exact=intervention.id)

                            is_editable_by_ip = {}
                            is_editable_by_ip[intervention.pk] = intervention.is_editable_by_ip(ip)

                            is_visible_by_ip = {}
                            is_visible_by_ip[intervention.pk] = intervention.is_visible_by_ip(ip)

                            # client_action_permissions = ClientActionPermissions(model=Client, user=request.user,
                            #                                                     enrolment=client)
                            intervention_action_permission = InterventionActionPermissions(model=Intervention,
                                                                                           user=request.user,
                                                                                           intervention=intervention, )
                            interventions_action_permissions = {
                                'can_perform_edit': intervention_action_permission.can_perform_edit(),
                                'can_perform_void': intervention_action_permission.can_perform_void()}

                            response_data = {
                                'status': 'success',
                                'message': 'Intervention successfully saved',
                                'intervention': serializers.serialize('json', [intervention, ], ensure_ascii=False),
                                'i_type': serializers.serialize('json', [intervention_type]),
                                'hts_results': serializers.serialize('json', htsresult),
                                'pregnancy_results': serializers.serialize('json', pregnancytestresult),
                                'permissions': json.dumps({
                                    'can_change_intervention': request.user.has_perm('DreamsApp.change_intervention'),
                                    'can_delete_intervention': request.user.has_perm('DreamsApp.delete_intervention')
                                }),
                                'is_editable_by_ip': is_editable_by_ip,
                                'is_visible_by_ip': is_visible_by_ip,
                                'client_is_exited': intervention.client.exited,
                                'intervention_action_permissions': interventions_action_permissions,
                                'implementing_partner_name': intervention.implementing_partner.name
                            }
                            return JsonResponse(response_data)

                else:  # Invalid Intervention Type
                    response_data = {
                        'status': 'fail',
                        'message': "Error: Invalid Intervention Type. "
                                   "Please select a valid Intervention Type to Proceed"
                    }
                return JsonResponse(response_data)

            else:  # User has no valid IP.
                response_data = {
                    'status': 'fail',
                    'message': "Error: You do not belong to an Implementing Partner. "
                               "Please contact your system admin to add you to the relevant Implementing Partner."
                }
                return JsonResponse(response_data)
        else:
            response_data = {
                'status': 'fail',
                'message': "Permission Denied: You don't have permission to Add Intervention"
            }
            return JsonResponse(response_data)
    except ImplementingPartnerUser.DoesNotExist:
        response_data = {
            'status': 'fail',
            'message': "Error: You do not belong to an Implementing Partner. "
                       "Please contact your system admin to add you to the relevant Implementing Partner."
        }
        return JsonResponse(response_data)
    except Exception as e:
        # check if validation error
        if type(e) is ValidationError:
            errormsg = '; '.join(ValidationError(e).messages)
        else:
            errormsg = str(e)

        response_data = {
            'status': 'fail',
            'message': errormsg
        }
        return JsonResponse(response_data)


def initiate_referral(request):
    try:
        if is_valid_post_request(request):
            OTHER_EXTERNAL_ORGANISATION_ID = ExternalOrganisation.objects.get(name='Other').pk
            client = Client.objects.filter(id__exact=int(request.POST.get('referral-client-id'))).first()
            source_implementing_partner = ImplementingPartner.objects.filter(
                id__exact=client.implementing_partner.id).first()
            intervention_type = InterventionType.objects.filter(
                code__exact=int(request.POST.get('referral-interventions-select'))).first()
            referral_date = request.POST.get('referral-date')
            expiry_date = request.POST.get('expiry-date')
            comment = request.POST.get('comment')
            to_external_organization = request.POST.get('to-external-organization')

            if not client:
                response_data = {
                    'status': 'fail',
                    'message': 'Client not found.'
                }
                return JsonResponse(response_data)

            if dt.strptime(str(referral_date), '%Y-%m-%d').date() > dt.now().date():
                response_data = {
                    'status': 'fail',
                    'message': 'Selected referral date cannot be later than today.'
                }
                return JsonResponse(response_data)

            if dt.strptime(str(referral_date), '%Y-%m-%d').date() < client.date_of_enrollment:
                response_data = {
                    'status': 'fail',
                    'message': 'Selected referral date cannot be earlier than client enrolment date.'
                }
                return JsonResponse(response_data)

            if dt.strptime(str(referral_date), '%Y-%m-%d').date() > dt.strptime(str(expiry_date), '%Y-%m-%d').date():
                response_data = {
                    'status': 'fail',
                    'message': 'Selected referral date cannot be later than referral expiry date.'
                }
                return JsonResponse(response_data)

            if bool(to_external_organization):
                if not request.POST.get('referral-external-organization-select') and not request.POST.get(
                        'other-organization-name'):
                    response_data = {
                        'status': 'fail',
                        'message': 'Select or input value for external organisation.'
                    }
                    return JsonResponse(response_data)

                if int(request.POST.get(
                        'referral-external-organization-select')) == OTHER_EXTERNAL_ORGANISATION_ID and not request.POST.get(
                    'other-organization-name'):
                    response_data = {
                        'status': 'fail',
                        'message': 'Input value for other external organisation.'
                    }
                    return JsonResponse(response_data)

            else:
                if not request.POST.get('implementing-partners-select'):
                    response_data = {
                        'status': 'fail',
                        'message': 'Select or input value for external organisation.'
                    }
                    return JsonResponse(response_data)

            if request.user.has_perm('DreamsApp.add_referral'):
                referral = Referral()
                referral.client = client
                referral.referring_ip = source_implementing_partner
                referral.intervention_type = intervention_type
                referral.referral_status = ReferralStatus.objects.get(name='Pending')
                referral.referral_date = referral_date
                referral.referral_expiration_date = expiry_date
                referral.comments = comment

                if bool(to_external_organization):
                    if request.POST.get('referral-external-organization-select'):
                        referral.external_organisation = ExternalOrganisation.objects.filter(
                            id__exact=int(request.POST.get('referral-external-organization-select'))).first()

                        if int(request.POST.get(
                                'referral-external-organization-select')) == OTHER_EXTERNAL_ORGANISATION_ID:
                            if request.POST.get('other-organization-name'):
                                referral.external_organisation_other = request.POST.get('other-organization-name')
                    else:
                        if request.POST.get('other-organization-name'):
                            referral.external_organisation_other = request.POST.get('other-organization-name')
                else:
                    referral.receiving_ip = ImplementingPartner.objects.filter(
                        id__exact=int(request.POST.get('implementing-partners-select'))).first()

                referral.save()
                response_data = {
                    'status': 'success',
                    'message': 'Referral added'
                }
                return JsonResponse(response_data)
            else:
                raise PermissionDenied

    except Exception as e:
        return HttpResponseServerError(e)


def get_all_intervention_types(request):
    try:
        if is_valid_get_request(request):
            intervention_types = InterventionType.objects.all()
            response_data = {
                'intervention_types': serializers.serialize('json', intervention_types)
            }
            return JsonResponse(response_data)
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def get_implementing_partners(request):
    try:
        if is_valid_get_request(request):
            if has_get_arg('referral-client-id', request):
                client_id = int(request.GET.get('referral-client-id'))
                client_implementing_partner = Client.objects.get(id=client_id).implementing_partner
                implementing_partners = ImplementingPartner.objects.exclude(id=client_implementing_partner.id)
                response_data = {
                    'implementing_partners': serializers.serialize('json', implementing_partners)
                }
                return JsonResponse(response_data)
            else:
                return ValueError('Client ID is required')
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def has_get_arg(arg_name, request):
    return arg_name in request.GET or request.GET.get(arg_name)


def get_intervention_list(request):
    try:
        user = request.user
        if request.method == 'POST' and user is not None and user.is_authenticated() and user.is_active:
            if 'client_id' not in request.POST or request.POST.get('client_id') == 0:
                return ValueError('No Client id found in your request! Ensure it is provided')
            if 'intervention_category_code' not in request.POST or request.POST.get('intervention_category_code') == 0:
                return ValueError('No Intervention Category Code found in your request! Ensure it is provided')

            client_id = request.POST.get('client_id')
            intervention_category_code = request.POST.get('intervention_category_code')
            iv_category = InterventionCategory.objects.get(code__exact=intervention_category_code)

            list_of_related_iv_types = iv_category.interventiontype_set.all()

            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    return HttpResponseServerError(e)

            # list_of_related_iv_types = InterventionType.objects.filter(intervention_category__exact=iv_category)
            iv_type_ids = [i_type.id for i_type in list_of_related_iv_types]
            # check for see_other_ip_data persmission
            intervention_type_category_cache_key = 'client-{}-intervention-type-category-{}'.format(client_id,
                                                                                                    intervention_category_code)
            list_of_interventions = get_list_of_interventions(client_id, iv_type_ids,
                                                              intervention_type_category_cache_key)
            client_key = 'client-{}'.format(client_id)
            client_found = get_client_found(client_id, client_key)
            client_is_transferred_out = client_found.transferred_out(ip)
            if not request.user.has_perm('DreamsApp.can_view_cross_ip_data'):
                if client_is_transferred_out:
                    list_of_interventions = list_of_interventions.filter(implementing_partner_id=ip.id)

            if not request.user.has_perm('auth.can_view_older_records'):
                list_of_interventions = list_of_interventions.filter(date_created__range=
                                                                     [dt.now() - timedelta(days=31),
                                                                      dt.now()]
                                                                     )

            is_editable_by_ip = {}
            is_visible_by_ip = {}
            intervention_ip_names = {}
            # client_action_permissions = ClientActionPermissions(model=Client, user=request.user, enrolment=client_found)
            intervention_action_permissions = InterventionActionPermissions(model=Intervention, user=user)
            interventions_action_permissions = {}

            for i in list_of_interventions:
                is_editable_by_ip[i.pk] = i.is_editable_by_ip(ip)
                is_visible_by_ip[i.pk] = i.is_visible_by_ip(ip)
                intervention_ip_names[i.pk] = i.implementing_partner.name
                intervention_action_permissions.intervention = i
                current_actions_permissions = {
                    'can_perform_edit': intervention_action_permissions.can_perform_edit(),
                    'can_perform_void': intervention_action_permissions.can_perform_void()
                }
                interventions_action_permissions[i.pk] = current_actions_permissions

            response_data = {
                'iv_types': serializers.serialize('json', list_of_related_iv_types),
                'interventions': serializers.serialize('json', list_of_interventions),
                'hts_results': serializers.serialize('json', HTSResult.objects.all()),
                'pregnancy_results': serializers.serialize('json', PregnancyTestResult.objects.all()),
                'permissions': json.dumps({
                    'can_change_intervention': request.user.has_perm('DreamsApp.change_intervention'),
                    'can_delete_intervention': request.user.has_perm('DreamsApp.delete_intervention'),
                    'client_is_exited': client_found.exited
                }),
                'is_editable_by_ip': is_editable_by_ip,
                'is_visible_by_ip': is_visible_by_ip,
                'client_is_exited': client_found.exited,
                'intervention_ip_names': intervention_ip_names,
                'interventions_action_permissions': interventions_action_permissions
            }
            return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


# Gets an intervention. Takes intervention_id and returns Intervention object
# use /ivGet/ to access this method

def get_list_of_interventions(client_id, iv_type_ids, cache_key):
    list_of_interventions = cache.get(cache_key)
    if not list_of_interventions:
        list_of_interventions = Intervention.objects.defer('date_changed', 'intervention_date',
                                                           'date_created').filter(client__exact=client_id,
                                                                                  intervention_type__in=iv_type_ids,
                                                                                  voided=False) \
            .order_by('-intervention_date', '-date_created', '-date_changed')
    cache_value(cache_key, list_of_interventions)
    return list_of_interventions


def get_client_found(client_id, client_key):
    try:
        client_found = cache.get(client_key)
        if not client_found:
            client_found = Client.objects.get(id=client_id)
        cache_value(client_key, client_found)
        return client_found
    except Exception as e:
        return None


def get_intervention(request):
    try:
        if request.method == 'POST' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
            intervention_id = request.POST.get('intervention_id')
            if 'intervention_id' not in request.POST:
                return ValueError('No intervention id found in your request!')
            intervention = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created').get(
                id__exact=intervention_id)
            if intervention is not None:
                response_data = {'intervention': serializers.serialize('json', [intervention, ])}
                return JsonResponse(response_data)
            else:
                raise Exception
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def add_follow_up(request):
    try:
        if is_valid_post_request(request):
            client_id = int(request.POST['client'], 0)
            client = Client.objects.get(id=client_id)

            follow_up_type = ClientFollowUpType.objects.filter(id__exact=request.POST.get('follow_up_type')).first()
            follow_up_result_type = ClientLTFUResultType.objects.filter(
                id__exact=request.POST.get('follow_up_result_type')).first()
            follow_up_date = request.POST.get('follow_up_date')
            follow_up_comments = request.POST.get('follow_up_comments')

            if not client or client.exited:
                response_data = {
                    'status': 'fail',
                    'message': 'There is no client found or the client has been exited.'
                }
                return JsonResponse(response_data)
            current_user_belongs_to_same_ip_as_client = client.current_user_belongs_to_same_ip_as_client(
                request.user.implementingpartneruser.implementing_partner_id)

            if not current_user_belongs_to_same_ip_as_client:
                response_data = {
                    'status': 'fail',
                    'message': 'Current user must belong to the same IP as the client.'
                }
                return JsonResponse(response_data)

            if dt.strptime(str(follow_up_date), '%Y-%m-%d').date() > dt.now().date():
                response_data = {
                    'status': 'fail',
                    'message': 'Selected follow up date cannot be later than today.'
                }
                return JsonResponse(response_data)

            if dt.strptime(str(follow_up_date), '%Y-%m-%d').date() < client.date_of_enrollment:
                response_data = {
                    'status': 'fail',
                    'message': 'Selected follow up date cannot be earlier than client enrolment date.'
                }
                return JsonResponse(response_data)

            add_follow_up_perm = FollowUpsServiceLayer(request.user)
            if not add_follow_up_perm.can_create_followup():
                response_data = {
                    'status': 'fail',
                    'message': 'You do not have permission to add a followup.'
                }
                return JsonResponse(response_data)

            if follow_up_type is not None \
                    and follow_up_result_type is not None \
                    and follow_up_date is not None:

                follow_up = ClientFollowUp()
                follow_up.client = client
                follow_up.date_of_followup = follow_up_date
                follow_up.type_of_followup = follow_up_type
                follow_up.result_of_followup = follow_up_result_type
                follow_up.comment = follow_up_comments
                follow_up.save()

                response_data = {
                    'status': 'success',
                    'message': 'Follow up details added'
                }
            else:
                response_data = {
                    'status': 'fail',
                    'message': 'Error with submitted follow up details'
                }
    except Exception as e:
        if type(e) is ValidationError:
            errormsg = '; '.join(ValidationError(e).messages)
        else:
            errormsg = str(e)

        response_data = {
            'status': 'fail',
            'message': "An error has occurred: " + errormsg
        }

    return JsonResponse(response_data)


def update_follow_up(request):
    try:
        if is_valid_post_request(request):
            follow_up_id = int(request.POST['follow_up_id'])
            follow_up = ClientFollowUp.objects.get(id=follow_up_id)

            if follow_up is not None:
                client = follow_up.client

                if not client or client.exited:
                    response_data = {
                        'status': 'fail',
                        'message': 'There is no client found or the client has been exited.'
                    }
                    return JsonResponse(response_data)
                current_user_belongs_to_same_ip_as_client = client.current_user_belongs_to_same_ip_as_client(
                    request.user.implementingpartneruser.implementing_partner_id)

                if not current_user_belongs_to_same_ip_as_client:
                    response_data = {
                        'status': 'fail',
                        'message': 'Current user must belong to the same IP as the client.'
                    }
                    return JsonResponse(response_data)

                edit_follow_up_perm = FollowUpsServiceLayer(request.user)
                if not edit_follow_up_perm.can_edit_followup():
                    response_data = {
                        'status': 'fail',
                        'message': 'You do not have permission to edit a followup.'
                    }
                    return JsonResponse(response_data)

                follow_up_type = ClientFollowUpType.objects.get(id__exact=request.POST.get('follow_up_type'))
                follow_up_result_type = ClientLTFUResultType.objects.get(
                    id__exact=request.POST.get('follow_up_result_type'))
                follow_up_date = request.POST.get('edit_follow_up_date')
                follow_up_comments = request.POST.get('follow_up_comments')

                if dt.strptime(str(follow_up_date), '%Y-%m-%d').date() > dt.now().date():
                    response_data = {
                        'status': 'fail',
                        'message': 'Selected follow up date cannot be later than today.'
                    }
                    return JsonResponse(response_data)

                if dt.strptime(str(follow_up_date), '%Y-%m-%d').date() < client.date_of_enrollment:
                    response_data = {
                        'status': 'fail',
                        'message': 'Selected follow up date cannot be earlier than client enrolment date.'
                    }
                    return JsonResponse(response_data)

                if follow_up_type is not None \
                        and follow_up_result_type is not None \
                        and follow_up_date is not None:

                    follow_up.date_of_followup = follow_up_date
                    follow_up.type_of_followup = follow_up_type
                    follow_up.result_of_followup = follow_up_result_type
                    follow_up.comment = follow_up_comments
                    follow_up.save()

                    response_data = {
                        'status': 'success',
                        'message': 'Follow up details updated'
                    }
                else:
                    response_data = {
                        'status': 'fail',
                        'message': 'Error with submitted follow up details'
                    }
            else:
                response_data = {
                    'status': 'fail',
                    'message': "Error follow up not found"
                }
    except Exception as e:
        if type(e) is ValidationError:
            errormsg = '; '.join(ValidationError(e).messages)
        else:
            errormsg = str(e)

        response_data = {
            'status': 'fail',
            'message': "An error has occurred: " + errormsg
        }

    return JsonResponse(response_data)


def update_intervention(request):
    try:
        user = request.user
        if request.method == 'POST' and user is not None and user.is_authenticated() and \
                request.user.is_active and request.user.has_perm('DreamsApp.change_intervention'):

            # Check if user belongs to an Ip
            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail',
                        'message': "You do not belong to any implementing partner"
                    }
                    return JsonResponse(response_data)

            if ip is not None:
                intervention_id = int(request.POST.get('intervention_id'))
                if intervention_id is not None and type(intervention_id) is int:
                    intervention = Intervention.objects.get(id__exact=intervention_id)

                    if not intervention.is_editable_by_ip(ip) or intervention.client.exited:
                        raise Exception(
                            'You do not have the rights to update this intervention or the client has been exited.'
                        )

                    # check if intervention belongs to the ip
                    if intervention.implementing_partner == ip:
                        # intervention.intervention_type = InterventionType.objects.get(
                        #     code__exact=int(request.POST.get('intervention_type_code')))
                        # intervention.client = Client.objects.get(id__exact=int(request.POST.get('client')))

                        intervention_date = dt.strptime(request.POST.get('intervention_date'), '%Y-%m-%d').date()

                        # check if external organisation is selected
                        external_organization_checkbox = request.POST.get('external_organization_checkbox')
                        external_organization_code = request.POST.get('external_organization_code')
                        other_external_organization_code = request.POST.get('other_external_organization_code')

                        if external_organization_checkbox:
                            if not external_organization_code:
                                response_data = {
                                    'status': 'fail',
                                    'message': "Error: External organisation must be selected if checkbox is checked."
                                }
                                return JsonResponse(response_data)
                        else:
                            if intervention.client.date_of_enrollment is not None and intervention_date < intervention.client.date_of_enrollment:
                                response_data = {
                                    'status': 'fail',
                                    'message': "Error: The intervention date must be after the client's enrollment date. "
                                }
                                return JsonResponse(response_data)

                        intervention.name_specified = request.POST.get('other_specify',
                                                                       '') if intervention.intervention_type.is_specified else ''
                        intervention.intervention_date = str(intervention_date)
                        intervention.changed_by = User.objects.get(id__exact=int(request.POST.get('changed_by')))
                        intervention.date_changed = dt.now()
                        intervention.comment = request.POST.get('comment')

                        # i_type = InterventionType.objects.get(id__exact=intervention.intervention_type.id)
                        i_type = intervention.intervention_type

                        htsresult = HTSResult.objects.all()
                        pregnancytestresult = PregnancyTestResult.objects.all()

                        if i_type.has_hts_result:
                            if request.POST.get('hts_result'):
                                intervention.hts_result = htsresult.get(
                                    code__exact=int(request.POST.get('hts_result')))

                        if i_type.has_pregnancy_result:
                            if request.POST.get('pregnancy_test_result'):
                                intervention.pregnancy_test_result = pregnancytestresult.get(
                                    code__exact=int(request.POST.get('pregnancy_test_result')))

                        if i_type.has_ccc_number:
                            intervention.client_ccc_number = request.POST.get('client_ccc_number')

                        if i_type.has_no_of_sessions:
                            intervention.no_of_sessions_attended = request.POST.get('no_of_sessions_attended')

                        if external_organization_checkbox:
                            intervention.external_organisation = ExternalOrganisation.objects.get(
                                pk=external_organization_code)
                            if other_external_organization_code:
                                intervention.external_organisation_other = other_external_organization_code
                            else:
                                intervention.external_organisation_other = None

                        intervention.save(user_id=user.id, action="UPDATE")  # Logging

                        intervention_type_category_cache_key = (
                            'client-{}-intervention-type-category-{}'.format(intervention.client.id,
                                                                             intervention.intervention_type.intervention_category.code))
                        cache.delete(intervention_type_category_cache_key)
                        # using defer() miraculously solved serialization problem of datetime properties.
                        # intervention = Intervention.objects.defer('date_changed', 'intervention_date',
                        #                                           'date_created').get(id__exact=intervention.id)
                        # construct response

                        response_data = {
                            'status': 'success',
                            'message': 'Intervention successfully updated',
                            'intervention': serializers.serialize('json', [intervention, ], ensure_ascii=False),
                            'i_type': serializers.serialize('json', [i_type]),
                            'hts_results': serializers.serialize('json', htsresult),
                            'pregnancy_results': serializers.serialize('json', pregnancytestresult),
                            'permissions': json.dumps({
                                'can_change_intervention': request.user.has_perm('DreamsApp.change_intervention'),
                                'can_delete_intervention': request.user.has_perm('DreamsApp.delete_intervention'),
                                'client_is_exited': intervention.client.exited
                            }),
                            'client_is_exited': intervention.client.exited
                        }
                    else:
                        # Intervention does not belong to Implementing partner. Send back error message
                        raise Exception(
                            'You do not have the rights to update this intervention because it was created by a '
                            'different Implementing Partner'
                        )
                    return JsonResponse(response_data)
                else:
                    raise Exception("Error: No intervention selected for update")
            else:  # Raise an exception. User does not belong to any IP
                raise Exception("Error: You do not belong to an Implementing Partner. "
                                "Please contact your system admin to add you to the relevant Implementing Partner.")
        else:
            response_data = {
                'status': 'fail',
                'message': "You Cannot edit interventions. Please contact System Administrator for help."
            }
            return JsonResponse(response_data)
    except Exception as e:
        # check if validation error
        if type(e) is ValidationError:
            errormsg = '; '.join(ValidationError(e).messages)
        else:
            errormsg = str(e)

        response_data = {
            'status': 'fail',
            'message': "An error has occurred: " + errormsg
        }
        return JsonResponse(response_data)


def delete_follow_up(request):
    try:
        if is_valid_post_request(request):
            follow_up_id = int(request.POST.get('follow_up_id'))

            if follow_up_id is not None and type(follow_up_id) is int:
                follow_up = ClientFollowUp.objects.filter(pk=follow_up_id).first()

                if follow_up is not None:
                    client = follow_up.client

                    if not client or client.exited:
                        response_data = {
                            'status': 'fail',
                            'message': 'There is no client found or the client has been exited.'
                        }
                        return JsonResponse(response_data)

                    delete_follow_up_perm = FollowUpsServiceLayer(request.user)
                    if not delete_follow_up_perm.can_delete_followup():
                        response_data = {
                            'status': 'fail',
                            'message': 'You do not have permission to delete a followup.'
                        }
                        return JsonResponse(response_data)

                    ClientFollowUp.objects.filter(pk=follow_up_id).delete()
                    log_custom_actions(request.user.id, "DreamsApp_clientfollowup", follow_up_id, "DELETE", None)

                    response_data = {
                        'status': 'success',
                        'message': 'Follow up has been successfully deleted',
                        'follow_up_id': follow_up_id
                    }
                    return JsonResponse(response_data)
                else:
                    response_data = {
                        'status': 'fail',
                        'message': 'Follow up not found'
                    }
                    return JsonResponse(response_data)

    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': "An error occurred while processing request. "
                       "Please contact the System Administrator if this error persists."
        }
        return JsonResponse(response_data)


def delete_intervention(request):
    try:
        user = request.user
        if request.method == 'POST' and user is not None and user.is_authenticated() and \
                user.is_active and user.has_perm('DreamsApp.delete_intervention'):

            # Check if user belongs to an Ip
            ip = None
            try:
                ip = user.implementingpartneruser.implementing_partner
            except Exception as e:
                if not ip:
                    response_data = {
                        'status': 'fail',
                        'message': "You do not belong to any implementing partner"
                    }
                    return JsonResponse(response_data)

            if ip is not None:
                intervention_id = int(request.POST.get('intervention_delete_id'))
                if intervention_id is not None and type(intervention_id) is int:
                    # get intervention
                    # Check if intervention belongs to IP
                    intervention_key = 'intervention-id-{}'.format(intervention_id)
                    intervention = cache.get(intervention_key)
                    if not intervention:
                        intervention = Intervention.objects.get(pk=intervention_id)
                    cache_value(intervention_key, intervention)

                    if not intervention.is_editable_by_ip(ip) or intervention.client.exited:
                        response_data = {
                            'status': 'fail',
                            'message': 'You do not have the rights to delete this intervention or the client has been exited.'
                        }
                        return JsonResponse(response_data)

                    if intervention.implementing_partner == ip:
                        intervention.voided = True
                        intervention.voided_by = request.user
                        intervention.date_voided = datetime.now()
                        intervention.save(user_id=request.user.id, action="UPDATE")  # Updating logs
                        intervention_type_category_cache_key = 'client-{}-intervention-type-category-{}'.format(
                            intervention.client.id, intervention.intervention_type.intervention_category.code)
                        cache.delete(intervention_type_category_cache_key)
                        # intervention.delete() # No deletion whatsoever
                        log_custom_actions(request.user.id, "DreamsApp_intervention", intervention_id, "DELETE", None)
                        response_data = {
                            'status': 'success',
                            'message': 'Intervention has been successfully deleted',
                            'intervention_id': intervention_id
                        }
                        return JsonResponse(response_data)
                    else:
                        response_data = {
                            'status': 'fail',
                            'message': 'You do not have the rights to delete this intervention because it was created by a '
                                       'different Implementing Partner'
                        }
                        return JsonResponse(response_data)
                else:
                    response_data = {
                        'status': 'fail',
                        'message': "Error: No intervention selected for deletion"
                    }
                    return JsonResponse(response_data)
            else:
                response_data = {
                    'status': 'fail',
                    'message': "Error: You do not belong to an Implementing Partner. "
                               "Please contact your system admin to add you to the relevant Implementing Partner."
                }
                return JsonResponse(response_data)
        else:
            response_data = {
                'status': 'fail',
                'message': "You don't have permission to delete Intervention. Please contact System Administrator for help."
            }
            return JsonResponse(response_data)
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': "An error occurred while processing request. "
                       "Contact System Administrator if this error Persists."
        }
        return JsonResponse(response_data)


def get_sub_counties(request):
    try:
        if request.method == 'GET' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
            response_data = {}
            county_id = request.GET['county_id']
            county_key = 'county-id-{}'.format(county_id)
            county = cache.get(county_key)
            if not county:
                county = County.objects.get(id__exact=county_id)
            cache_value(county_key, county)

            sub_county_key = 'county-id-{}-sub_counties'.format(county_id)
            sub_counties = cache.get(sub_county_key)
            if not sub_counties:
                sub_counties = county.subcounty_set.all()
            cache_value(sub_county_key, sub_counties)
            sub_counties = serializers.serialize('json', sub_counties)
            response_data["sub_counties"] = sub_counties
            return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def get_wards(request):
    if request.method == 'GET' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
        response_data = {}
        sub_county_id = request.GET['sub_county_id']
        sub_county_key = 'sub-county-id-{0}'.format(sub_county_id)
        sub_county = cache.get(sub_county_key)
        if not sub_county:
            sub_county = SubCounty.objects.get(id__exact=sub_county_id)
        cache_value(sub_county_key, sub_county)
        ward_key = 'sub-county-id-{}-wards'.format(sub_county_id)
        wards = cache.get(ward_key)
        if not wards:
            wards = sub_county.ward_set.all()
        cache_value(ward_key, wards)
        wards = serializers.serialize('json', wards)
        response_data["wards"] = wards
        return JsonResponse(response_data)

    else:
        raise PermissionDenied


def log_me_out(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('login')
    else:
        raise PermissionDenied


def reporting(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'GET':
                return render(request, 'reporting.html', {'user': request.user, 'page_title': 'DREAMS Reporting', })
            elif request.method == 'POST' and request.is_ajax():
                return render(request, 'reporting.html', {'user': request.user, 'page_title': 'DREAMS Reporting', })
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc()
        return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception


def user_help(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'GET':
                return render(request, 'help.html', {
                    'user': request.user,
                    'page': 'help',
                    'page_title': 'DREAMS User help'
                })
            elif request.method == 'POST' and request.is_ajax():
                return render(request, 'help.html', {
                    'user': request.user,
                    'page': 'help',
                    'page_title': 'DREAMS User help'
                })
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def user_help_download(request):
    if request.user.is_authenticated() and request.user.is_active:
        try:
            manual_filename = request.POST.get('manual') if request.method == 'POST' else request.GET.get('manual')
            manual_friendly_name = request.POST.get(
                'manual_friendly_name') if request.method == 'POST' else request.GET.get('manual_friendly_name')
            fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, '../templates', 'manuals'))
            filename = manual_filename + '.pdf'
            if fs.exists(filename):
                with fs.open(filename, 'rb') as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="' + manual_friendly_name + '"'
                    return response
            else:
                raise "The manual for " + manual_friendly_name + " is not found"
        except Exception as e:
            raise e
    else:
        raise PermissionDenied


def logs(request):
    user = request.user
    if user.is_authenticated() and user.is_active:
        if not user.is_superuser and not user.has_perm('DreamsApp.can_manage_audit'):
            raise PermissionDenied('Operation not allowed. [Missing Permission]')

        try:
            ip = user.implementingpartneruser.implementing_partner.id
        except ImplementingPartnerUser.DoesNotExist:
            return HttpResponseServerError("You do not belong to an implementing partner.")

        # user is allowed to view logs
        if request.method == 'GET':
            try:
                page = request.GET.get('page', 1)
                filter_text = request.GET.get('filter-log-text', '')
                filter_date_from = request.GET.get('filter-log-date-from', '')
                filter_date_to = request.GET.get('filter-log-date', '')

                # getting logs
                if filter_text:
                    logs = Audit.objects.filter(
                        reduce(operator.or_, (Q(table__icontains=item) for item in filter_text.split(" "))) |
                        reduce(operator.or_, (Q(action__icontains=item) for item in filter_text.split(" "))) |
                        reduce(operator.or_, (Q(search_text__icontains=item) for item in filter_text.split(" "))) |
                        reduce(operator.or_, (Q(user__username__icontains=item) for item in filter_text.split(" "))) |
                        reduce(operator.or_, (Q(user__first_name__icontains=item) for item in filter_text.split(" "))) |
                        reduce(operator.or_, (Q(user__last_name__icontains=item) for item in filter_text.split(" ")))
                    ).order_by('-timestamp')
                else:
                    logs = Audit.objects.all().order_by('-timestamp')

                logs = filter_audit_logs_by_date_and_ip(filter_date_to, filter_date_from, ip, logs)
                paginator = Paginator(logs, 25)  # Showing 25 contacts per page
                try:
                    logs_list = paginator.page(page)
                except PageNotAnInteger:
                    logs_list = paginator.page(1)  # Deliver the first page is page is not an integer
                except EmptyPage:
                    logs_list = paginator.page(0)  # Deliver the last page if page is out of scope
                return render(request, 'log.html', {'page': 'logs', 'page_title': 'DREAMS Logs', 'logs': logs_list,
                                                    'filter_text': filter_text,
                                                    'filter_date_from': filter_date_from,
                                                    'filter_date': filter_date_to,
                                                    'items_in_page': 0 if logs_list.end_index() == 0 else
                                                    (logs_list.end_index() - logs_list.start_index() + 1)
                                                    }
                              )
            except Exception as e:
                tb = traceback.format_exc(e)
                return HttpResponseServerError(tb)
        else:
            raise bad_request(request)
    else:
        raise PermissionDenied


def filter_audit_logs_by_date_and_ip(filter_date_to, filter_date_from, ip, logs):
    if ip:
        logs = logs.filter(Q(user__implementingpartneruser__implementing_partner__id__exact=ip))
    if filter_date_from and not filter_date_to:
        fyr, fmnth, fdt = filter_date_from.split('-')
        constructed_date_from = date(int(fyr), int(fmnth), int(fdt))
        logs = logs.filter(Q(timestamp__gte=constructed_date_from))
    elif not filter_date_from and filter_date_to:
        yr, mnth, dat = filter_date_to.split('-')
        constructed_date = date(int(yr), int(mnth), int(dat))
        logs = logs.filter(Q(timestamp__lte=constructed_date))
    elif filter_date_from and filter_date_to:
        yr, mnth, dat = filter_date_to.split('-')
        constructed_date_to = date(int(yr), int(mnth), int(dat)) + timedelta(days=1)
        fyr, fmnth, fdt = filter_date_from.split('-')
        constructed_date_from = date(int(fyr), int(fmnth), int(fdt))
        logs = logs.filter(Q(timestamp__range=[constructed_date_from, constructed_date_to]))
    return logs


# user management
def users(request):
    if request.user.is_authenticated() and request.user.is_active and request.user.has_perm('auth.can_manage_user'):
        try:
            items_per_page = 15
            if request.method == 'GET':
                page = request.GET.get('page', 1)
                filter_text = request.GET.get('filter-user-text', '')
                ip_user_list = ImplementingPartnerUser.objects.filter(Q(user__first_name__contains=filter_text) |
                                                                      Q(user__last_name__contains=filter_text) |
                                                                      Q(user__username__contains=filter_text)
                                                                      ).order_by('-user__date_joined')
            elif request.method == 'POST':
                page = request.POST.get('page', 1)
                filter_text = request.POST.get('filter-user-text', '')
                # get list of users with the filter incorporated
                if filter_text is not u'' and filter_text is not " ":
                    ip_user_list = ImplementingPartnerUser.objects.filter(
                        Q(user__first_name__in=filter_text.split(" ")) |
                        Q(user__last_name__in=filter_text.split(" ")) |
                        Q(user__username__in=filter_text.split(" "))
                    ).order_by('-user__date_joined')
                else:
                    ip_user_list = ImplementingPartnerUser.objects.filter(Q(user__first_name__contains=filter_text) |
                                                                          Q(user__last_name__contains=filter_text) |
                                                                          Q(user__username__contains=filter_text)
                                                                          ).order_by('-user__date_joined')
            #  current user ip
            try:
                current_user_ip = request.user.implementingpartneruser.implementing_partner
            except ImplementingPartnerUser.DoesNotExist:
                current_user_ip = None
            except ImplementingPartner.DoesNotExist:
                current_user_ip = None
            if not request.user.has_perm('DreamsApp.can_view_cross_ip_data'):
                if current_user_ip is not None:
                    ip_user_list = ip_user_list.filter(implementing_partner=current_user_ip)
                else:
                    ip_user_list = ImplementingPartnerUser.objects.none()
            # do pagination
            paginator = Paginator(ip_user_list, items_per_page)
            final_ip_user_list = paginator.page(page)
        except ImplementingPartnerUser.DoesNotExist:
            current_user_ip = None
        except PageNotAnInteger:
            final_ip_user_list = paginator.page(1)  # Deliver the first page is page is not an integer
        except EmptyPage:
            final_ip_user_list = paginator.page(0)  # Deliver the last page if page is out of scope
        return render(request, 'users.html',
                      {'page': 'users', 'page_title': 'DREAMS User List', 'ip_users': final_ip_user_list,
                       'filter_text': filter_text,
                       'items_in_page': 0 if final_ip_user_list.end_index() == 0 else
                       (final_ip_user_list.end_index() - final_ip_user_list.start_index() + 1),
                       'implementing_partners': ImplementingPartner.objects.all(),
                       'current_user_ip': current_user_ip,
                       'roles': Group.objects.all()
                       })
    else:
        raise PermissionDenied  # this should be a redirection to the permissions denied page


def save_user(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated() and request.user.is_active and request.user.has_perm(
            'auth.can_manage_user'):
        try:
            new_user_ip = ImplementingPartner.objects.get(name=
                                                          request.POST.get('implementing_partner',
                                                                           ''))  # Valid IP for new user
            # check if user can change cross IP data
            if not request.user.has_perm('auth.can_change_cross_ip_data'):
                # User must register new user under their IP. Theck if user has a valid IP
                # check if registering user belongs to an IP
                ip = request.user.implementingpartneruser.implementing_partner
                if ip is None:  # Registering user does not belong to an IP. Raise exception
                    raise Exception("Error: You do not belong to an Implementing Partner. "
                                    "Please contact your system admin to add you to the relevant Implementing Partner.")

                elif new_user_ip != ip:
                    # Registering user and user do not belong to same IP. Raise exception
                    raise Exception(
                        "Error: You do not have permission to register a user under a different Implementing"
                        " partner other than " + request.user.implementingpartneruser.
                        implementing_partner.name)

            # Everything is fine. Proceed to register user
            # Check to see if IP user exists already or not
            ip_user_id = request.POST.get('ip_user_id', 0)
            if ip_user_id == 0 or ip_user_id is None or ip_user_id == u'':
                # This is a new user
                username = request.POST.get('username', '')
                email = request.POST.get('emailaddress', '')
                role = request.POST.get('role', '')
                # Check if provided username is in db
                try:
                    user = User.objects.get(username__exact=username)
                    raise Exception("Error: The username '" + username +
                                    "' is already take. Please enter a different username and continue")
                except User.DoesNotExist:
                    # user with this username does not exist
                    user_group = Group.objects.filter(name__exact=role).first()  # get group
                    user = User.objects.create_user(
                        username=username, email=email, password='PTZ%hz^+&mny+9Av'
                    )
                    user.first_name = request.POST.get('firstname', '')
                    user.last_name = request.POST.get('lastname', '')
                    user.groups.add(user_group)
                    user.save()  # save user changes first
                    ip_user = ImplementingPartnerUser.objects.create(
                        user=user,
                        implementing_partner=new_user_ip
                    )
                    try:
                        # send email with user credentials
                        msg = EmailMessage('DREAMS Credentials',
                                           'Dear ' + user.first_name + ',\n\n Welcome to DREAMS. You can login to your account at http://dreams-dev.globalhealthapp.net.'
                                                                       '\n\n\t Username: ' + username +
                                           '\n\t Password:  PTZ%hz^+&mny+9Av'
                                           '\n\nThank you,'
                                           '\nDREAMS Administrator',
                                           to=[email])
                        msg.send()
                        response_data = {
                            'status': 'success',
                            'message': 'User successfully saved. Your temporary password has been sent to ' + email,
                            'ip_users': serializers.serialize('json', [ip_user, ])
                        }
                        return JsonResponse(response_data)
                    except Exception as e:
                        response_data = {
                            'status': 'success',
                            'message': 'User registered but could not send login detais to provided email address. '
                                       'Contact System Admin for help ',
                            'ip_users': serializers.serialize('json', [ip_user, ])
                        }
                        return JsonResponse(response_data)
            else:  # raise exception
                raise Exception('User with id ' + ip_user_id + ' exists already')
        except ImplementingPartner.DoesNotExist:
            # User being registered under invalid IP. Raise an error
            raise Exception("Error: User must be registered under an Implementing Partner")

        except Exception as e:
            response_data = {
                'status': 'fail',
                'message': "An error occurred while processing request. Contact System Administrator if this error Persists.",
                'ip_users': ''
            }
            return JsonResponse(response_data)
    else:
        raise PermissionDenied


def toggle_status(request):
    try:
        if request.method == 'GET' and request.user is not None and request.user.is_authenticated() \
                and request.user.is_active and request.user.has_perm('auth.can_change_user_status'):
            if request.method == 'GET':
                ip_user_id = request.GET.get('ip_user_id', 0)
                toggle = str(request.GET.get('toggle', False))
                #  get ip user
                ip_user = ImplementingPartnerUser.objects.filter(id__exact=ip_user_id).first()
                if ip_user is not None:
                    # Get user object
                    user = User.objects.filter(id__exact=ip_user.user.id).first()
                    if user is not None:
                        # check if user is same as requesting user
                        if user.id == request.user.id:
                            raise Exception('Error: you cannot deactivate your own account. '
                                            'Please contact System Administrator for assistance')
                        else:
                            user.is_active = toggle in ["True", "true", 1, "Yes", "yes", "Y", "y", "T", "t"]
                            user.save()
                            # return success message
                            response_data = {
                                'status': 'success',
                                'message': 'User status changed successfully'
                            }
                            return JsonResponse(response_data)
                    else:
                        raise Exception('Error: you did not select a valid user. Please try again')
                else:
                    raise Exception('Error: you did not select a valid user. Please try again')
            else:
                raise Exception("Invalid user request!")
        else:
            raise Exception('Error: You do not have permission to perform this operation. Please contact your server '
                            'administrator for assistance')
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': "An error occurred while processing request. Contact System Administrator if this error Persists."
        }
        return JsonResponse(response_data)


def change_cred(request):
    if request.user.is_authenticated() and request.user.is_active:  # user is authenticated
        if request.method == 'GET':
            context = {'page': 'account', 'page_title': 'DREAMS Password Change', 'user': request.user, }
            return render(request, 'change_cred.html', context)
        elif request.method == 'POST':
            ch_username = request.POST.get('ch_username', '')
            ch_current_password = request.POST.get('ch_current_password', '')
            ch_new_password = request.POST.get('ch_new_password', '')
            ch_confirm_new_password = request.POST.get('ch_confirm_new_password', '')
            if ch_username == '' or ch_current_password == '' or ch_new_password == '' or ch_confirm_new_password == '' or ch_confirm_new_password == '':
                response_data = {
                    'status': 'fail',
                    'message': 'An error occurred as a result of missing details.'
                }
                return JsonResponse(response_data)
            else:
                if request.user.get_username() == ch_username and request.user.check_password(
                        ch_current_password) and ch_new_password == ch_confirm_new_password:
                    request.user.set_password(ch_new_password)
                    request.user.save()
                    response_data = {
                        'status': 'success',
                        'message': 'Password changed successfully. Proceed to login with your new credentials'
                    }
                    return JsonResponse(response_data)

                else:
                    response_data = {
                        'status': 'fail',
                        'message': 'An error occurred as a result of wrong credentials.'
                    }
                    return JsonResponse(response_data)

    else:  # User is not logged in. Redirect user to login page
        # return PermissionDenied('Operation not allowed. [Missing Permission]')
        raise PermissionDenied


def bad_request(request):
    context = {'user': request.user, 'error_code': 400, 'error_title': 'Bad Request (Error 400)',
               'error_message':
                   'Your browser sent a request that this server could not understand. '}
    return render(request, 'error_page.html', context)


def permission_denied(request):
    context = {'user': request.user, 'error_code': 403, 'error_title': 'Permission Denied (Error 403)',
               'error_message':
                   'You do not have permission to view this page [Missing Permission]. '
                   'Go back to previous page or Home page'}
    return render(request, 'error_page.html', context)


def page_not_found(request):
    context = {'user': request.user, 'error_code': 404, 'error_title': 'Page Not Found (Error 404)',
               'error_message': 'The page you are looking for does not exist. Go back to previous page or Home page'}
    return render(request, 'error_page.html', context)


def server_error(request):
    context = {'user': request.user, 'error_code': 500, 'error_title': 'Server Error (Error 500)',
               'error_message':
                   'A server error occurred while processing your request. Please try again or contact your '
                   'administrator if the error persists. '}
    return render(request, 'error_page.html', context)


def grievances_list(request):
    try:
        if not request.user.is_authenticated():
            raise PermissionDenied
        page = request.GET.get('page', 1) if request.method == 'GET' else request.POST.get('page', 1)
        filter_date = request.GET.get('filter_date', None) if request.method == 'GET' else request.POST.get(
            'filter_date', None)
        filter_text = request.GET.get('filter-user-text', '') if request.method == 'GET' else request.POST.get(
            'filter-user-text', '')
        try:
            user_ip = request.user.implementingpartneruser.implementing_partner
        except:
            user_ip = None
        """ IP level permission check """
        grievance_list = Grievance.objects.all() if request.user.has_perm('DreamsApp.can_view_cross_ip_data') else \
            Grievance.objects.filter(implementing_partner=user_ip)
        """Date filter """
        if filter_date is not None and filter_date is not u'':
            yr, mnth, dt = filter_date.split('-')
            constructed_date = date(int(yr), int(mnth), int(dt))
            grievance_list = Grievance.objects.filter(Q(date__year=constructed_date.year,
                                                        date__month=constructed_date.month,
                                                        date__day=constructed_date.day))
        """ Text filter """
        # if filter_text is not u'' and filter_text is not '':
        # grievance_list = Grievance.objects.filter(Q(reporter_name__contains=filter_text) |
        #                                         Q(relationship__containts=filter_text) |
        #                                        Q(reporter_phone__contains=filter_text))
        # do pagination
        try:
            paginator = Paginator(grievance_list, 20)
            final_grievance_list = paginator.page(page)
        except PageNotAnInteger:
            final_grievance_list = paginator.page(1)  # Deliver the first page is page is not an integer
        except EmptyPage:
            final_grievance_list = paginator.page(0)  # Deliver the last page if page is out of scope
        response_data = {
            'page': 'cash_transfer', 'page_title': 'DREAMS Grievance List',
            'filter_text': filter_text,
            'filter_date': filter_date,
            'items_in_page': 0 if final_grievance_list.end_index() == 0 else
            (final_grievance_list.end_index() - final_grievance_list.start_index() + 1),
            'current_user_ip': user_ip,
            'form': GrievanceModelForm(current_user=request.user),
            'grievance_list': final_grievance_list,
            'status': 'success'
        }
        return render(request, 'grievances.html', response_data)
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': "An error occurred while processing request. Contact System Administrator if this error Persists."
        }
        return JsonResponse(response_data)


@csrf_exempt
def grievances_create(request):
    try:
        if request.user.is_authenticated() and request.method == 'POST' and request.is_ajax():
            grievance = GrievanceModelForm(request.POST, current_user=request.user)
            if grievance.is_valid():
                saved_grievance = grievance.save(commit=False)
                saved_grievance.created_by = request.user
                saved_grievance.save()
                response_data = {
                    'status': 'success',
                    'message': 'Grievance saved successfully',
                    'grievance': grievance.data,
                    'grievance_id': saved_grievance.id,
                    'reporter_categories': serializers.serialize('json', GrievanceReporterCategory.objects.all()),
                    'grievance_nature': serializers.serialize('json', GrievanceNature.objects.all()),
                    'status_list': serializers.serialize('json', GrievanceStatus.objects.all()),
                }
                return JsonResponse(response_data)
            else:
                raise Exception(grievance.errors)
        else:
            raise PermissionDenied
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': "An error occurred while processing request. Contact System Administrator if this error Persists."
        }
        return JsonResponse(response_data)


@csrf_exempt
def grievances_edit(request):
    """ """
    try:
        if request.user.is_authenticated() and request.method == 'POST' and request.is_ajax():
            try:
                id = int(request.POST.get('id', 0))
                instance = Grievance.objects.get(id=id)
                form = GrievanceModelForm(request.POST, instance=instance, current_user=request.user)
                if not form.is_valid():
                    response_data = {
                        'status': 'fail',
                        'message': form.errors
                    }
                else:
                    saved_grievance = form.save(commit=False)
                    saved_grievance.changed_by = request.user
                    saved_grievance.save()
                    response_data = {
                        'status': 'success',
                        'message': 'Grievance edited successfully',
                        'grievance': form.data,
                        'reporter_categories': serializers.serialize('json', GrievanceReporterCategory.objects.all()),
                        'grievance_nature': serializers.serialize('json', GrievanceNature.objects.all()),
                        'status_list': serializers.serialize('json', GrievanceStatus.objects.all()),
                    }
                    return JsonResponse(response_data)
            except Grievance.DoesNotExist:
                response_data = {
                    'status': 'fail',
                    'message': 'Grievance not found'
                }
                return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': "An error occurred while processing request. Contact System Administrator if this error Persists."
        }
        return JsonResponse(response_data)


@csrf_exempt
def grievances_delete(request):
    """ """
    try:
        if request.user.is_authenticated() and request.method == 'POST' and request.is_ajax():
            try:
                id = int(request.POST.get('id', 0))
                instance = Grievance.objects.get(id=id).delete()
                response_data = {
                    'status': 'success',
                    'message': 'Grievance deleted successfully',
                    'grievanceId': id
                }
                return JsonResponse(response_data)
            except Grievance.DoesNotExist:
                response_data = {
                    'status': 'fail',
                    'message': 'Grievance not found'
                }
                return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': "An error occurred while processing request. Contact System Administrator if this error Persists."
        }
        return JsonResponse(response_data)


def grievances_get(request):
    """ """
    try:
        if not request.user.is_authenticated():
            raise PermissionDenied
        grievance_id = request.GET.get('grievance_id', 0) if request.method == 'GET' else request.POST.get(
            'grievance_id', 0)
        try:
            grievance = Grievance.objects.get(id__exact=grievance_id)
            response_data = {
                'status': 'success',
                'message': 'Grievance saved successfully',
                'grievance': serializers.serialize('json', [grievance]),
            }
        except Grievance.DoesNotExist:
            response_data = {
                'status': 'fail',
                'message': 'Grievance not found in Database'
            }
        return JsonResponse(response_data)
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': "An error occurred while processing request. Contact System Administrator if this error Persists."
        }
        return JsonResponse(response_data)


@csrf_exempt
def cash_transfer_details_save(request):
    try:
        if request.user.is_authenticated() and request.method == 'POST' and request.is_ajax():
            # check if details has id
            id = request.POST.get('id', 0)
            if id not in [u'', "0", 0, ""]:
                id = int(id)
                ct_detail = ClientCashTransferDetails.objects.get(id=id)
                ct_form = ClientCashTransferDetailsForm(request.POST, instance=ct_detail)
            else:
                # get current AGYW
                ct_form = ClientCashTransferDetailsForm(request.POST)
            if ct_form.is_valid():
                saved_detail = ct_form.save(commit=False)
                if saved_detail.id is not None and saved_detail.id > 0:
                    saved_detail.changed_by = request.user
                else:
                    saved_detail.created_by = request.user
                saved_detail.save()
                response_data = {
                    'status': 'success',
                    'message': 'Cash Transfer details updated successfully',
                    'ct_detail_id': saved_detail.id,
                }
                return JsonResponse(response_data)
            else:
                raise Exception(ct_form.errors)
        else:
            raise PermissionDenied
    except ClientCashTransferDetails.DoesNotExist:
        raise Exception("Cash transfer details does not exist for editing!")
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': "An error occurred while processing request. Contact System Administrator if this error Persists."
        }
        return JsonResponse(response_data)


def export_page(request):
    if request.user.is_authenticated() and request.user.is_active and request.user.has_perm(
            'DreamsApp.can_export_raw_data'):

        try:
            ips = None
            ip_user = request.user.implementingpartneruser
            if request.user.is_superuser or request.user.has_perm('DreamsApp.can_view_cross_ip_data'):
                ips = ImplementingPartner.objects.all()

            elif request.user.implementingpartneruser is not None:
                ips = ImplementingPartner.objects.filter(
                    id=request.user.implementingpartneruser.implementing_partner.id)

                if ips.count() > 0:
                    sub_grantees = ImplementingPartner.objects.filter(parent_implementing_partner__in=ips)
                    if sub_grantees.exists():
                        ips = ips.union(sub_grantees)

            context = {'page': 'export', 'page_title': 'Client Raw Enrolment Export', 'ips': ips,
                       'counties': County.objects.all()}

            return render(request, 'dataExport.html', context)
        except ImplementingPartnerUser.DoesNotExist:
            traceback.format_exc()
        except ImplementingPartner.DoesNotExist:
            traceback.format_exc()
    else:
        raise PermissionDenied


def intervention_export_page(request):
    if request.user.is_authenticated() and request.user.is_active and request.user.has_perm(
            'DreamsApp.can_export_raw_data'):

        try:
            ips = None
            if request.user.is_superuser or request.user.has_perm('DreamsApp.can_view_cross_ip_data'):
                ips = ImplementingPartner.objects.all()
            elif request.user.implementingpartneruser is not None:
                ips = ImplementingPartner.objects.filter(
                    id=request.user.implementingpartneruser.implementing_partner.id)

                if ips.count() > 0:
                    sub_grantees = ImplementingPartner.objects.filter(parent_implementing_partner__in=ips)
                    if sub_grantees.exists():
                        ips = ips.union(sub_grantees)

            context = {'page': 'export', 'page_title': 'Client Interventions Export', 'ips': ips,
                       'counties': County.objects.all()}
            return render(request, 'interventionDataExport.html', context)
        except ImplementingPartnerUser.DoesNotExist:
            traceback.format_exc()
        except ImplementingPartner.DoesNotExist:
            traceback.format_exc()
    else:
        raise PermissionDenied


def download_raw_enrollment_export(request):
    try:
        ip_list_str = request.POST.getlist('ips')
        sub_county = request.POST.get('sub_county')
        ward = request.POST.get('ward')
        county = request.POST.get('county_of_residence')
        from_date = request.POST.get('from_date')
        end_date = request.POST.get('to_date')

        params = request.POST
        validation_errors = {}

        from .form_validations import validate_from_date, validate_to_date
        validate_to_date(params, validation_errors)
        validate_from_date(params, validation_errors)

        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)
            return render(request, 'idataExport.html', {form: params, errors: validation_errors})

        export_file_name = urllib.parse.quote(
            ("/tmp/raw_enrolment_export-{}.csv").format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        export_doc = DreamsRawExportTemplateRenderer()

        if request.user.is_superuser or request.user.has_perm('DreamsApp.can_view_phi_data') \
                or Permission.objects.filter(group__user=request.user).filter(
            codename='DreamsApp.can_view_phi_data').exists():
            show_PHI = True
        else:
            show_PHI = False

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment; filename="{}"').format(export_file_name)
        export_doc.prepare_enrolment_export_doc(response, ip_list_str, county, sub_county, ward, show_PHI, from_date,
                                                end_date)

        return response

    except Exception as e:
        traceback.format_exc()
        return


def download_raw_intervention_export(request):
    try:
        ip_list_str = request.POST.getlist('ips')
        sub_county = request.POST.get('sub_county')
        ward = request.POST.get('ward')
        county = request.POST.get('county_of_residence')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        from_date = datetime.strptime(from_date, '%Y-%m-%d').date() if from_date else None
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date() if to_date else None

        params = request.POST
        validation_errors = {}

        from .form_validations import validate_from_date, validate_to_date
        validate_to_date(params, validation_errors)
        validate_from_date(params, validation_errors)

        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)
            return render(request, 'interventionDataExport.html', {form: params, errors: validation_errors})

        export_file_name = urllib.parse.quote(
            "/tmp/raw_intervention_export-{}.csv".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        export_doc = DreamsRawExportTemplateRenderer()

        show_PHI = request.user.is_superuser or request.user.has_perm('DreamsApp.can_view_phi_data') \
                   or Permission.objects.filter(group__user=request.user).filter(
            codename='DreamsApp.can_view_phi_data').exists()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment; filename="{}"').format(export_file_name)

        export_doc.get_intervention_export_doc(response, ip_list_str, county, sub_county, ward, show_PHI, from_date,
                                               to_date)

        return response
    except ValidationError as e:
        print(e)
    except Exception as e:
        traceback.format_exc()
        return


def individual_service_layering_export_page(request):
    if request.user.is_authenticated() and request.user.is_active and request.user.has_perm(
            'DreamsApp.can_export_raw_data'):

        try:
            ips = None
            if request.user.is_superuser or request.user.has_perm('DreamsApp.can_view_cross_ip_data'):
                ips = ImplementingPartner.objects.all()
            elif request.user.implementingpartneruser is not None:
                ips = ImplementingPartner.objects.filter(
                    id=request.user.implementingpartneruser.implementing_partner.id)

                if ips.count() > 0:
                    sub_grantees = ImplementingPartner.objects.filter(parent_implementing_partner__in=ips)
                    if sub_grantees.exists():
                        ips = ips.union(sub_grantees)

            context = {'page': 'export', 'page_title': 'Service Layering Export', 'ips': ips,
                       'counties': County.objects.all()}
            return render(request, 'individualServiceLayeringDataExport.html', context)

        except ImplementingPartnerUser.DoesNotExist:
            traceback.format_exc()
        except ImplementingPartner.DoesNotExist:
            traceback.format_exc()
    else:
        raise PermissionDenied


def download_services_received_export(request):
    try:
        ip_list_str = request.POST.getlist('ips')
        sub_county = request.POST.get('sub_county')
        ward = request.POST.get('ward')
        county = request.POST.get('county_of_residence')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        from_date = datetime.strptime(from_date, '%Y-%m-%d').date() if from_date else None
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date() if to_date else None

        params = request.POST
        validation_errors = {}

        from .form_validations import validate_from_date, validate_to_date
        validate_to_date(params, validation_errors)
        validate_from_date(params, validation_errors)

        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)
            return render(request, 'individualServiceLayeringDataExport.html',
                          {form: params, errors: validation_errors})

        export_file_name = urllib.parse.quote(
            ("/tmp/services_received_export-{}.csv").format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        export_doc = DreamsRawExportTemplateRenderer()

        if request.user.is_superuser or request.user.has_perm('DreamsApp.can_view_phi_data') \
                or Permission.objects.filter(group__user=request.user).filter(
            codename='DreamsApp.can_view_phi_data').exists():
            show_PHI = True
        else:
            show_PHI = False

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment; filename="{}"').format(export_file_name)
        export_doc.get_individual_export_doc(response, ip_list_str, county, sub_county, ward, show_PHI, from_date,
                                             to_date)
        return response

    except Exception as e:
        traceback.format_exc()
        return


def transfer_client(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'POST' and request.is_ajax():
                try:
                    ip = request.user.implementingpartneruser.implementing_partner
                except (ImplementingPartnerUser.DoesNotExist, ImplementingPartner.DoesNotExist):
                    response_data = {
                        'status': 'fail',
                        'message': 'Transfer Failed. You do not belong to an implementing partner',
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)

                transfer_form = ClientTransferForm(request.POST)
                if transfer_form.is_valid():
                    client = transfer_form.instance.client
                    if not client or client.exited:
                        response_data = {
                            'status': 'fail',
                            'message': 'There is no client found or the client has been exited.'
                        }
                        return JsonResponse(response_data)
                    current_user_belongs_to_same_ip_as_client = client.current_user_belongs_to_same_ip_as_client(
                        request.user.implementingpartneruser.implementing_partner_id) or request.user.is_superuser
                    initiate_transfer_perm = TransferServiceLayer(request.user)
                    if not initiate_transfer_perm.can_initiate_transfer() and current_user_belongs_to_same_ip_as_client:
                        response_data = {
                            'status': 'fail',
                            'message': 'You do not have permission to initiate a tranfer.'
                        }
                        return JsonResponse(response_data)

                    num_of_pending_transfers = ClientTransfer.objects.filter(client=transfer_form.instance.client,
                                                                             transfer_status=ClientTransferStatus.objects.get(
                                                                                 code__exact=TRANSFER_INITIATED_STATUS)).count()

                    if num_of_pending_transfers > 0:
                        print("{} pending transfers for client".format(num_of_pending_transfers))
                        response_data = {
                            'status': 'fail',
                            'message': "Transfer failed, there's a pending transfer for this client.",
                        }
                    else:
                        client_transfer = transfer_form.save(commit=False)
                        client_transfer.transfer_status = ClientTransferStatus.objects.get(
                            code__exact=TRANSFER_INITIATED_STATUS)
                        client_transfer.source_implementing_partner = ip
                        client_transfer.initiated_by = request.user
                        client_transfer.start_date = dt.now()
                        client_transfer.save()

                        client = transfer_form.instance.client
                        client.date_changed = dt.now()
                        client.save()

                        response_data = {
                            'status': 'success',
                            'message': 'Transfer request received, pending approval by the receiving implementing partner.',
                        }
                    return JsonResponse(json.dumps(response_data), safe=False)
                else:
                    response_data = {
                        'status': 'fail',
                        'message': transfer_form.errors,
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)
        else:
            raise PermissionDenied
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': str(e),
        }
        return JsonResponse(json.dumps(response_data), safe=False)


def client_transfers(request, *args, **kwargs):
    if request.user is not None and request.user.is_authenticated() and request.user.is_active:
        transferred_in = bool(int(kwargs.pop('transferred_in', 1)))
        search_transfers_term = ''
        transfer_perm = TransferServiceLayer(request.user)
        can_accept_or_reject = transfer_perm.can_accept_or_reject_transfer()
        c_transfers = None
        try:
            ip = request.user.implementingpartneruser.implementing_partner
            if transferred_in:
                search_term = None
                if request.POST:
                    search_term = request.POST.get('search-transfers-term')
                    if search_term != '':
                        search_transfers_term = search_term
                        c_transfers = ClientTransfer.objects.filter(destination_implementing_partner=ip).select_related(
                            'client') \
                            .filter(Q(client__dreams_id__iexact=search_term)) \
                            .exclude(client__voided=True).order_by('transfer_status', '-date_created')
                    else:
                        search_transfers_term = ''
                        c_transfers = ClientTransfer.objects.filter(destination_implementing_partner=ip).order_by(
                            'transfer_status', '-date_created')
                else:
                    c_transfers = ClientTransfer.objects.filter(destination_implementing_partner=ip).order_by(
                        'transfer_status', '-date_created')
            else:
                c_transfers = ClientTransfer.objects.filter(source_implementing_partner=ip).order_by('transfer_status',
                                                                                                     '-date_created')

        except (ImplementingPartnerUser.DoesNotExist, ImplementingPartner.DoesNotExist):
            return render(request, 'login.html')

        page = request.GET.get('page', 1)
        paginator = Paginator(c_transfers, 20)

        try:
            transfers = paginator.page(page)
        except PageNotAnInteger:
            transfers = paginator.page(1)
        except EmptyPage:
            transfers = paginator.page(paginator.num_pages)

        return render(request, "client_transfers.html",
                      {'client_transfers': transfers, 'can_accept_or_reject': can_accept_or_reject,
                       'transferred_in': transferred_in, 'page': 'transfers',
                       'search_transfers_term': search_transfers_term})
    else:
        return redirect('login')

"""
def client_referrals(request, *args, **kwargs):
    user = request.user
    if user is not None and user.is_authenticated() and user.is_active:
        referred_in = bool(int(kwargs.pop('referred_in', 1)))
        referral_perm = ReferralServiceLayer(user)
        can_accept_or_reject = referral_perm.can_accept_or_reject_referral()

        try:
            ip = user.implementingpartneruser.implementing_partner
            if referred_in:
                client_referrals = Referral.objects.filter(Q(receiving_ip=ip) | (Q(referring_ip=ip) and (
                        Q(external_organisation__isnull=False) | Q(
                    external_organisation_other__isnull=False)))).order_by(
                    'referral_status', '-referral_date')
            else:
                client_referrals = Referral.objects.filter(Q(referring_ip=ip)).exclude((Q(referring_ip=ip) and (
                        Q(external_organisation__isnull=False) | Q(
                    external_organisation_other__isnull=False)))).order_by('referral_status', '-referral_date')

            for client_referral in client_referrals:
                try:
                    intervention = Intervention.objects.get(referral_id=client_referral.pk)
                except Exception:
                    intervention = None

                if intervention:
                    client_referral.receiving_ip_comment = intervention.comment
                else:
                    client_referral.receiving_ip_comment = ""

        except (ImplementingPartnerUser.DoesNotExist, ImplementingPartner.DoesNotExist):
            return render(request, 'login.html')

        page = request.GET.get('page', 1)
        paginator = Paginator(client_referrals, 20)

        try:
            referrals = paginator.page(page)
        except PageNotAnInteger:
            referrals = paginator.page(1)
        except EmptyPage:
            referrals = paginator.page(paginator.num_pages)

        return render(request,
                      "client_referrals.html",
                      {
                          'client_referrals': referrals,
                          'can_accept_or_reject': can_accept_or_reject,
                          'referred_in': referred_in,
                          'page': 'referrals',
                          'now': datetime.now().date()
                      })
    else:
        return redirect('login')
"""

class ClientReferralsListView(ListView):
    model = Referral
    template_name = 'client_referrals.html'

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientReferralsListView, self).get_context_data(**kwargs)
        context['to_login'] = False
        context['error'] = ''

        try:
            user = self.request.user
            if user is not None and user.is_authenticated() and user.is_active:
                referred_in = bool(int(kwargs.pop('referred_in', 1)))
                referral_perm = ReferralServiceLayer(user)
                can_accept_or_reject = referral_perm.can_accept_or_reject_referral()

                try:
                    ip = user.implementingpartneruser.implementing_partner
                    if referred_in:
                        client_referrals = Referral.objects.filter(Q(receiving_ip=ip) | (Q(referring_ip=ip) and (
                                Q(external_organisation__isnull=False) | Q(
                            external_organisation_other__isnull=False)))).order_by(
                            'referral_status', '-referral_date')
                    else:
                        client_referrals = Referral.objects.filter(Q(referring_ip=ip)).exclude((Q(referring_ip=ip) and (
                                Q(external_organisation__isnull=False) | Q(
                            external_organisation_other__isnull=False)))).order_by('referral_status', '-referral_date')

                    for client_referral in client_referrals:
                        try:
                            intervention = Intervention.objects.get(referral_id=client_referral.pk)
                        except Exception:
                            intervention = None

                        if intervention:
                            client_referral.receiving_ip_comment = intervention.comment
                        else:
                            client_referral.receiving_ip_comment = ""

                except (ImplementingPartnerUser.DoesNotExist, ImplementingPartner.DoesNotExist):
                    context['error'] = "User does not belong to any implementing partner"

                page = self.request.GET.get('page', 1)
                paginator = Paginator(client_referrals, 20)

                try:
                    referrals = paginator.page(page)
                except PageNotAnInteger:
                    referrals = paginator.page(1)
                except EmptyPage:
                    referrals = paginator.page(paginator.num_pages)

                context['client_referrals'] = referrals
                context['can_accept_or_reject'] = can_accept_or_reject
                context['referred_in'] = referred_in
                context['page'] = 'referrals'
                context['now'] = datetime.now().date()

            else:
                context['to_login'] = True

        except Exception as e:
            tb = traceback.format_exc(e)
            context['error'] = tb
        return context

    def render_to_response(self, context, **response_kwargs):
        if context['to_login']:
            return redirect('login')
        if context['error'] != '':
            return HttpResponseServerError(context['error'])
        return super(ClientReferralsListView, self).render_to_response(context, **response_kwargs)

    def get_queryset(self):
        return Client.objects.none()


def accept_client_transfer(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'POST':

                try:
                    ip = request.user.implementingpartneruser.implementing_partner
                except (ImplementingPartnerUser.DoesNotExist, ImplementingPartner.DoesNotExist):
                    if not request.user.is_superuser:
                        messages.error(request, "You do not belong to an implementing partner")
                        return redirect(reverse("client_transfers", kwargs={'transferred_in': 1}))
                    else:
                        ip = None

                client_transfer_id = request.POST.get("id", "")
                if client_transfer_id != "":
                    client_transfer = ClientTransfer.objects.get(id__exact=client_transfer_id)
                    client = client_transfer.client

                    if client and not client.exited:
                        transfer_perm = TransferServiceLayer(request.user, client_transfer=client_transfer)
                        can_accept_transfer = transfer_perm.can_accept_transfer()

                        if not can_accept_transfer:
                            raise PermissionDenied

                        if client_transfer is not None:
                            accepted_client_transfer_status = ClientTransferStatus.objects.get(
                                code__exact=TRANSFER_ACCEPTED_STATUS)

                            client_transfer.transfer_status = accepted_client_transfer_status
                            client_transfer.completed_by = request.user
                            client_transfer.end_date = dt.now()

                            # Update the client to receive interventions from this new ip.
                            client = Client.objects.get(id__exact=client_transfer.client.id)
                            if ip is None and request.user.is_superuser:
                                ip = client_transfer.destination_implementing_partner
                            client.implementing_partner = ip

                            with transaction.atomic():
                                client.save()
                                client_transfer.save()

                            messages.info(request, "Transfer successfully accepted.")
                            return redirect("/client?client_id={}".format(client.id))
                        else:
                            messages.error(request,
                                           "Transfer not effected. There is no client or the client has been exited.")

                    else:
                        messages.error(request,
                                       "Transfer not effected. Contact System Administrator if this error Persists.")

                else:
                    messages.error(request,
                                   "Transfer not effected. Contact System Administrator if this error Persists.")
        else:
            raise PermissionDenied
    except Exception as e:
        messages.error(request,
                       "An error occurred while processing request. "
                       "Contact System Administrator if this error Persists.")

    return redirect(reverse("client_transfers", kwargs={'transferred_in': 1}))


def reject_client_transfer(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'POST':

                client_transfer_id = request.POST.get("id", "")
                if client_transfer_id != "":
                    client_transfer = ClientTransfer.objects.get(id__exact=client_transfer_id)
                else:
                    client_transfer = None

                if client_transfer is not None:
                    transfer_perm = TransferServiceLayer(request.user, client_transfer=client_transfer)
                    can_reject_transfer = transfer_perm.can_reject_transfer()

                    if not can_reject_transfer:
                        raise PermissionDenied

                    client_transfer.transfer_status = ClientTransferStatus.objects.get(
                        code__exact=TRANSFER_REJECTED_STATUS)
                    client_transfer.completed_by = request.user
                    client_transfer.end_date = dt.now()
                    client_transfer.save()

                    messages.info(request, "Transfer successfully rejected.")
                else:
                    messages.warning(request,
                                     "Transfer not rejected. Contact System Administrator if this error Persists.")
        else:
            raise PermissionDenied
    except Exception as e:
        messages.error(request,
                       "An error occurred while processing request. "
                       "Contact System Administrator if this error Persists.")

    return redirect(reverse("client_transfers", kwargs={'transferred_in': 1}))


def reject_client_referral(request):
    try:
        if is_valid_post_request(request):
            user = request.user
            client_referral_id = request.POST.get("id", "")
            reject_reason = request.POST.get("reject_reason", "")

            if reject_reason and reject_reason.strip():
                if client_referral_id:
                    client_referral = Referral.objects.get(id__exact=client_referral_id)

                    if client_referral is not None:
                        referral_perm = ReferralServiceLayer(user, client_referral=client_referral)
                        if not referral_perm.can_reject_referral():
                            raise PermissionDenied

                        if client_referral.referral_expiration_date >= dt.now().date():
                            client_referral.referral_status = ReferralStatus.objects.get(
                                code__exact=REFERRAL_REJECTED_STATUS)
                            client_referral.completed_by = user
                            client_referral.end_date = dt.now()
                            client_referral.rejectreason = reject_reason
                            client_referral.save()
                            messages.info(request, "Referral successfully rejected.")
                        else:
                            messages.error(request,
                                           "This referral has already expired and cannot be rejected.")
                    else:
                        messages.error(request,
                                       "Referral does not exist.")
                else:
                    messages.error(request,
                                   "Invalid referral ID.")
            else:
                messages.error(request,
                               "Input value for reason to reject referral.")
        else:
            raise PermissionDenied
    except Exception as e:
        messages.error(request,
                       "An error occurred while processing request. "
                       "Contact System Administrator if this error Persists.")

    return redirect(reverse("client_referrals", kwargs={'referred_in': 1}))


def get_pending_client_transfers_total_count(request):
    client_transfers_total_count = 0
    if request.user is not None and request.user.is_authenticated() and request.user.is_active:
        initiated_client_transfer_status = ClientTransferStatus.objects.get(code__exact=TRANSFER_INITIATED_STATUS)
        try:
            ip = request.user.implementingpartneruser.implementing_partner
            client_transfers_total_count = ClientTransfer.objects.filter(
                Q(destination_implementing_partner=ip) | Q(source_implementing_partner=ip),
                transfer_status=initiated_client_transfer_status).count()

        except Exception:
            client_transfers_total_count = 0
    return HttpResponse(client_transfers_total_count)


def get_pending_client_transfers_in_out_count(request):
    client_transfers_count_array = [0, 0]
    if request.user is not None and request.user.is_authenticated() and request.user.is_active:
        initiated_client_transfer_status = ClientTransferStatus.objects.get(code__exact=TRANSFER_INITIATED_STATUS)
        try:
            ip = request.user.implementingpartneruser.implementing_partner
            client_transfers_in_count = ClientTransfer.objects.filter(
                destination_implementing_partner=ip,
                transfer_status=initiated_client_transfer_status).count()
            client_transfers_out_count = ClientTransfer.objects.filter(
                source_implementing_partner=ip,
                transfer_status=initiated_client_transfer_status).count()

            client_transfers_count_array = [client_transfers_in_count, client_transfers_out_count]
        except:
            client_transfers_count_array = [0, 0]
    return HttpResponse(json.dumps(client_transfers_count_array))


def get_pending_client_referrals_total_count(request):
    client_referrals_total_count = 0
    if request.user is not None and request.user.is_authenticated() and request.user.is_active:
        try:
            pending_client_referral_status = ReferralStatus.objects.get(code__exact=REFERRAL_PENDING_STATUS)
            ip = request.user.implementingpartneruser.implementing_partner
            client_referrals_total_count = Referral.objects.filter(
                referral_status=pending_client_referral_status and (Q(receiving_ip=ip) | (Q(referring_ip=ip)))).filter(
                client__exited=False).filter(referral_expiration_date__gte=datetime.now().date()).count()
        except:
            client_referrals_total_count = 0
    return HttpResponse(client_referrals_total_count)


def get_pending_client_referrals_in_out_count(request):
    client_referrals_count_array = [0, 0]
    user = request.user
    if user is not None and user.is_authenticated() and user.is_active:
        pending_client_referral_status = ReferralStatus.objects.get(code__exact=REFERRAL_PENDING_STATUS)
        try:
            ip = user.implementingpartneruser.implementing_partner
            client_referrals_in_count = Referral.objects.filter(
                referral_status=pending_client_referral_status and (Q(receiving_ip=ip) | (Q(referring_ip=ip) and (
                        Q(external_organisation__isnull=False) | Q(
                    external_organisation_other__isnull=False))))).filter(client__exited=False).filter(
                referral_expiration_date__gte=datetime.now().date()).count()
            client_referrals_out_count = Referral.objects.filter(
                referral_status=pending_client_referral_status and (Q(referring_ip=ip))).exclude(
                Q(referring_ip=ip) and (
                        Q(external_organisation__isnull=False) | Q(
                    external_organisation_other__isnull=False))).filter(client__exited=False).filter(
                referral_expiration_date__gte=datetime.now().date()).count()

            client_referrals_count_array = [client_referrals_in_count, client_referrals_out_count]
        except Exception:
            client_referrals_count_array = [0, 0]
    return HttpResponse(json.dumps(client_referrals_count_array))


def intervention_export_transferred_in_page(request):
    if request.user.is_authenticated() and request.user.is_active and request.user.has_perm(
            'DreamsApp.can_export_raw_data'):

        try:
            ips = None
            if request.user.is_superuser or request.user.has_perm('DreamsApp.can_view_cross_ip_data'):
                ips = ImplementingPartner.objects.all()
            elif request.user.implementingpartneruser is not None:
                ips = ImplementingPartner.objects.filter(
                    id=request.user.implementingpartneruser.implementing_partner.id)
            if ips.count() > 0:
                ips = ips.union(ImplementingPartner.objects.filter(parent_implementing_partner__in=ips))

            context = {'page': 'export', 'page_title': 'Interventions Transferred In Export', 'ips': ips,
                       'counties': County.objects.all()}
            return render(request, 'interventionDataExportTransferredIn.html', context)

        except (ImplementingPartnerUser.DoesNotExist, ImplementingPartner.DoesNotExist):
            traceback.format_exc()
    else:
        raise PermissionDenied


def download_raw_intervention_transferred_in_export(request):
    try:
        from_intervention_date = request.POST.get('from_intervention_date')
        to_intervention_date = request.POST.get('to_intervention_date')

        export_file_name = urllib.parse.quote(
            ("/tmp/raw_intervention_transferred_in_export-{}.csv").format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        export_doc = DreamsRawExportTemplateRenderer()

        if request.user.is_superuser or request.user.has_perm('DreamsApp.can_view_phi_data') \
                or Permission.objects.filter(group__user=request.user).filter(
            codename='DreamsApp.can_view_phi_data').exists():
            show_PHI = True
        else:
            show_PHI = False

        try:
            ip = request.user.implementingpartneruser.implementing_partner
        except (ImplementingPartnerUser.DoesNotExist, ImplementingPartner.DoesNotExist):
            ip = None

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = ('attachment; filename="{}"').format(export_file_name)
        export_doc.get_intervention_transferred_in_doc(response, ip, from_intervention_date, to_intervention_date,
                                                       show_PHI)
        return response

    except Exception as e:
        raise e


def export_client_transfers(request, *args, **kwargs):
    if request.user is not None and request.user.is_authenticated() and request.user.is_active:

        transferred_in = bool(int(kwargs.pop('transferred_in', 1)))
        columns = ("client__dreams_id", "source_implementing_partner__name",
                   "destination_implementing_partner__name", "transfer_reason", "transfer_status__name",)

        try:
            ip = request.user.implementingpartneruser.implementing_partner
            if transferred_in:
                c_transfers = ClientTransfer.objects.values(*columns).filter(destination_implementing_partner=ip)
            else:
                c_transfers = ClientTransfer.objects.values(*columns).filter(source_implementing_partner=ip)
        except (ImplementingPartnerUser.DoesNotExist, ImplementingPartner.DoesNotExist):
            c_transfers = ClientTransfer.objects.values(*columns)

        header = ['Dreams ID', 'Source Implementing Partner', 'Destination Implementing Partner', 'Transfer Reason',
                  'Status']

        export_file_name = urllib.parse.quote(
            "/tmp/client_transfers_export-{}.csv".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(export_file_name)

        writer = unicodecsv.DictWriter(response, fieldnames=columns, extrasaction='raise')
        header = dict(zip(columns, header))
        writer.writerow(header)

        for row in c_transfers:
            writer.writerow(row)

        return response
    else:
        return redirect('login')


def export_client_referrals(request, *args, **kwargs):
    user = request.user
    if user is not None and user.is_authenticated() and user.is_active:

        referred_in = bool(int(kwargs.pop('referred_in', 1)))
        columns = ("client__dreams_id", "referring_ip__name",
                   "external_organisation__name", "external_organisation_other", "intervention_type__name",
                   "referral_date", "referral_expiration_date", "referral_status__name",)

        try:
            ip = user.implementingpartneruser.implementing_partner
            if referred_in:
                c_referrals = Referral.objects.values(*columns).filter(Q(receiving_ip=ip) | (Q(referring_ip=ip) and (
                        Q(external_organisation__isnull=False) | Q(
                    external_organisation_other__isnull=False)))).order_by('referral_status', '-referral_date')
            else:
                c_referrals = Referral.objects.values(*columns).filter(referring_ip=ip).order_by('referral_status',
                                                                                                 '-referral_date')

        except (ImplementingPartnerUser.DoesNotExist, ImplementingPartner.DoesNotExist):
            c_referrals = Referral.objects.values(*columns)

        header = ['Dreams ID', 'Referring Implementing Partner', 'External Organisation', 'External Organisation Other',
                  'Intervention', 'Referral Date', 'Referral Expiration Date',
                  'Status']

        export_file_name = urllib.parse.quote(
            "/tmp/client_referrals_export-{}.csv".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(export_file_name)

        writer = unicodecsv.DictWriter(response, fieldnames=columns, extrasaction='raise')
        header = dict(zip(columns, header))
        writer.writerow(header)

        for row in c_referrals:
            writer.writerow(row)

        return response
    else:
        return redirect('login')


def void_client(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'POST' and request.is_ajax():
                if not request.user.is_superuser and not request.user.has_perm(
                        'DreamsApp.can_void_client') and not Permission.objects.filter(group__user=request.user).filter(
                    codename='DreamsApp.can_void_client').exists():
                    return get_response_data(0, 'Voiding Failed. You do not have permission to void a client')

                client_id = request.POST.get("id", "")
                client = Client.objects.get(id=client_id)
                current_user_belongs_to_same_ip_as_client = client.current_user_belongs_to_same_ip_as_client(
                    request.user.implementingpartneruser.implementing_partner_id)
                if not (current_user_belongs_to_same_ip_as_client or request.user.is_superuser):
                    response_data = {
                        'status': 'fail',
                        'errors': "Void failed. You must belong to the same IP as the client inorder to update"
                    }
                    return JsonResponse(response_data, status=500)

                void_reason = request.POST.get("void_reason", "")
                if void_reason is None or void_reason == "" or void_reason.isspace():
                    return get_response_data(0, {'void_reason': ['Reason for voiding is required.']})

                if client_id != "":
                    cursor = db_conn_2.cursor()
                    try:
                        args = [client_id, request.user.id, void_reason]
                        cursor.callproc('sp_void_client_by_id', args)
                        exec_status = cursor.fetchone()[0]

                        if exec_status == 1:
                            messages.info(request, "Client has been voided.")
                            response_data = get_response_data(1, 'Client has been voided.', next_url=reverse('clients'))
                        else:
                            response_data = get_response_data(0,
                                                              'Client not voided, please contact system '
                                                              'administrator for assistance.')
                    except Exception as e:
                        response_data = get_response_data(0, 'Client could not be voided.{}'.format(e))
                    finally:
                        cursor.close()

                    return response_data
                else:
                    return get_response_data(0, 'Invalid client ID. Please specify client.')
            else:
                raise SuspiciousOperation
        else:
            raise PermissionDenied
    except Exception as e:
        traceback.format_exc()
        return get_response_data(0, e)


def get_response_data(status, message, **kwargs):
    response = {
        'status': 'success' if status == 1 else 'fail',
        'message': message
    }

    for k, v in kwargs.items():
        response[k] = v

    return JsonResponse(json.dumps(response), safe=False)


def download_audit_logs(request):
    if not request.user.is_superuser and not request.user.has_perm('DreamsApp.can_manage_audit'):
        raise PermissionDenied('Operation not allowed. [Missing Permission]')

    ip = ''
    try:
        ip = request.user.implementingpartneruser.implementing_partner.id
    except ImplementingPartnerUser.DoesNotExist:
        pass

    # user is allowed to view logs
    if request.method == 'GET':
        try:
            filter_text = request.GET.get('filter-log-text', '')
            filter_date_from = request.GET.get('filter-log-date-from', '')
            filter_date_to = request.GET.get('filter-log-date', '')

            # getting logs
            if filter_text:
                logs = Audit.objects.filter(
                    reduce(operator.or_, (Q(table__icontains=item) for item in filter_text.split(" "))) |
                    reduce(operator.or_, (Q(action__icontains=item) for item in filter_text.split(" "))) |
                    reduce(operator.or_, (Q(search_text__icontains=item) for item in filter_text.split(" "))) |
                    reduce(operator.or_, (Q(user__username__icontains=item) for item in filter_text.split(" "))) |
                    reduce(operator.or_, (Q(user__first_name__icontains=item) for item in filter_text.split(" "))) |
                    reduce(operator.or_, (Q(user__last_name__icontains=item) for item in filter_text.split(" ")))
                ).order_by('-timestamp')
            else:
                logs = Audit.objects.all().order_by('-timestamp')

            logs = filter_audit_logs_by_date_and_ip(filter_date_to, filter_date_from, ip, logs).values()
            columns = ['timestamp', 'user_name', 'table', 'column', 'old_value', 'new_value', 'action', 'search_text']
            header = ['Timestamp', 'User', 'Table', 'Field', 'Old Value', 'New Value', 'Action', 'Text']

            export_file_name = urllib.parse.quote(
                "/tmp/audit_log_export-{}.csv".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(export_file_name)

            writer = unicodecsv.DictWriter(response, fieldnames=columns, extrasaction='raise')
            header = dict(zip(columns, header))
            writer.writerow(header)

            for log in logs:
                audittrail = AuditTrail.objects.filter(Q(audit_id=log['id'])).values()
                column = ""
                old_value = ""
                new_value = ""

                if len(audittrail) > 0:
                    column_keys = ['column', 'old_value', 'new_value']
                    column_values = [itemgetter(*column_keys)(x) for x in audittrail]
                    column = ', '.join([str(x[0]) for x in column_values])
                    old_value = ', '.join([str(x[1]) for x in column_values])
                    new_value = ', '.join([str(x[2]) for x in column_values])

                writer.writerow(
                    {'timestamp': log['timestamp'], 'user_name': get_user_name(log['user_id']), 'table': log['table'],
                     'column': column, 'old_value': old_value, 'new_value': new_value, 'action': log['action'],
                     'search_text': log['search_text']})

            return response

        except AttributeError:
            return HttpResponseServerError(AttributeError)
        except UnicodeEncodeError:
            return HttpResponseServerError(UnicodeEncodeError)
        except Exception as e:
            tb = traceback.format_exc(e)
            return HttpResponseServerError(tb)
    else:
        raise SuspiciousOperation


def get_user_name(user_id):
    if not user_id:
        return ''
    else:
        user = User.objects.get(id=user_id)
        if not user:
            return ''

        full_name = user.get_full_name()
        return full_name if full_name else full_name


def get_min_max_date_of_birth(request):
    try:
        if request.method == 'POST' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
            date_of_enrollment_str = request.POST.get('date_of_enrollment')
            date_of_enrollment = datetime.strptime(str(date_of_enrollment_str),
                                                   '%Y-%m-%d').date() if date_of_enrollment_str is not None else dt.now().date()
            client_enrolment_service_layer = ClientEnrolmentServiceLayer(request.user)
            minimum_maximum_age = client_enrolment_service_layer.get_minimum_maximum_enrolment_age(
                client_enrolment_service_layer.ENROLMENT_CUTOFF_DATE)
            max_dob = date_of_enrollment - relativedelta(years=int(minimum_maximum_age[0]))
            min_dob = date_of_enrollment - relativedelta(years=int(minimum_maximum_age[1]) + 1) + timedelta(days=1)

            response_data = {
                "min_dob": min_dob,
                "max_dob": max_dob
            }
            return JsonResponse(response_data)

        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def cache_value(key, value):
    cache_time = 86400  # time in seconds for cache to be valid
    cache.set(key, value, cache_time)
