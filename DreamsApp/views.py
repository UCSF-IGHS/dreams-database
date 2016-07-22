from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, HttpResponseRedirect
from django.core import serializers
from django.core.exceptions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
import json
import traceback
from datetime import date, timedelta
from django.db.models import Q
from DreamsApp.forms import *
from DreamsApp.models import *
from DreamsApp.Dreams_Utils import *


def get_enrollment_form_config_data():
    config_data = {
        'implementing_partners': ImplementingPartner.objects.all(),
        'verification_documents': VerificationDocument.objects.all(),
        'marital_status': MaritalStatus.objects.all(),
        'counties': County.objects.all()
        #  'sub_counties': SubCounty.objects.all(),
        #  'wards': Ward.objects.all()
    }
    return config_data


def log_custom_actions(user_id, table, row_id, action, search_text):
    audit = Audit()
    audit.user_id = user_id
    audit.table = table
    audit.row_id = row_id
    audit.action = action
    audit.search_text = search_text
    audit.save()


def user_login(request):

    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user_name = request.POST.get('inputUsername', '')
        pass_word = request.POST.get('inputPassword', '')

        audit = Audit()
        audit.user_id = 0
        audit.table = "DreamsApp_client"
        audit.row_id = 0
        audit.action = "LOGIN"
        #
        # response_data = {
        #     'status': 'success',
        #     'message': 'Client Details Deleted successfuly.'
        # }

        if user_name == '' or pass_word == '':
            audit.search_text = "Missing login Credentials"
            audit.save()
            response_data = {
                'status': 'fail',
                'message': 'Missing username or password.'
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


def clients(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'GET':
                client_list = Client.objects.filter(id__exact=0)   # Clients list should be empty on start
                implementing_partner_user = ImplementingPartnerUser.objects.filter(user=request.user).first()
                context = {'page': 'clients', 'user': request.user, 'clients': client_list,
                           'implementing_partner_user': implementing_partner_user,
                           'config_data': get_enrollment_form_config_data()}
                return render(request, 'clients.html', context)
            elif request.method == 'POST':
                search_value = request.POST.get('searchValue', '')

                if request.user.has_perm('auth.can_search_client_by_name'):
                    search_result = Client.objects.filter(Q(dreams_id__exact=search_value) |
                                                          Q(first_name__exact=search_value) |
                                                          Q(last_name__exact=search_value) |
                                                          Q(middle_name__exact=search_value))
                else:
                    search_result = Client.objects.filter(dreams_id__exact=search_value)
                # check if user can see clients enrolled more than a week ago
                log_custom_actions(request.user.id, "DreamsApp_client", None, "SEARCH", search_value)
                return JsonResponse(serializers.serialize('json', search_result), safe=False)
        else:
            return redirect('login')
    except Exception as e:
        return redirect('login')


def client_profile(request):
    if request.user is not None and request.user.is_authenticated() and request.user.is_active:
        if request.method == 'GET':
            client_id = int(request.GET['client_id'])
        else:
            client_id = int(request.POST('client_id', ''))

        if client_id is not None and client_id != 0:
            try:
                client_found = Client.objects.get(id=client_id)
                if client_found is not None:
                    return render(request, 'client_profile.html', {'page': 'clients', 'client': client_found, 'user': request.user})
            except:
                return render(request, 'login.html')
    return render(request, 'login.html')


def save_client(request):
    try:
        if request.user is not None and request.user.is_authenticated():
            if request.method == 'GET':
                return render(request, 'enrollment.html', {'client': None})
            elif request.method == 'POST' and request.is_ajax():
                # process saving user
                client = Client.objects.create(
                    implementing_partner=ImplementingPartner.objects.filter(
                        code__exact=request.POST.get('implementing_partner', '')).first(),
                    first_name=request.POST.get('first_name', ''),
                    middle_name=request.POST.get('middle_name', ''),
                    last_name=request.POST.get('last_name', ''),
                    date_of_birth=request.POST.get('date_of_birth', ''),
                    is_date_of_birth_estimated=request.POST.get('is_date_of_birth_estimated', ''),
                    verification_document=VerificationDocument.objects.filter(
                        code__exact=request.POST.get('verification_document', '')).first(),
                    verification_doc_no=request.POST.get('verification_doc_no', ''),
                    date_of_enrollment=request.POST.get('date_of_enrollment', ''),
                    age_at_enrollment=int(request.POST.get('age_at_enrollment', 10)),
                    marital_status=MaritalStatus.objects.filter(code__exact=str(request.POST.get('marital_status', ''))).first(),
                    phone_number=request.POST.get('phone_number', ''),
                    dss_id_number=request.POST.get('dss_id_number', ''),
                    county_of_residence=County.objects.filter(code__exact=request.POST.get('county_of_residence', '')).first(),
                    sub_county=SubCounty.objects.filter(code__exact=request.POST.get('sub_county', '')).first(),
                    ward=Ward.objects.filter(code__exact=request.POST.get('ward', '')).first(),
                    informal_settlement=request.POST.get('informal_settlement', ''),
                    village=request.POST.get('village', ''),
                    landmark=request.POST.get('landmark', ''),
                    dreams_id=request.POST.get('dreams_id', ''),
                    guardian_name=request.POST.get('guardian_name', ''),
                    relationship_with_guardian=request.POST.get('relationship_with_guardian', ''),
                    guardian_phone_number=request.POST.get('guardian_phone_number', ''),
                    guardian_national_id=request.POST.get('guardian_national_id', ''),
                    enrolled_by=request.user
                )
                client.save(user_id=request.user.id, action="INSERT")
                if request.is_ajax():
                    response_data = {
                        'status': 'success',
                        'message': 'Enrollment to DREAMS successful.',
                        'client_id': client.id
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)
                else:
                    # redirect to page
                    return redirect('clients')
        else:
            return PermissionDenied('Operation not allowed. [Missing Permission]')
    except Exception as e:
        tb = traceback.format_exc()
        return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception


def edit_client(request):
    try:
        if request.user is not None and request.user.is_authenticated():  # and request.user.is_superuser:
            if request.method == 'GET':
                client_id = int(request.GET['client_id'])
                client = Client.objects.defer('date_of_enrollment', 'date_of_birth').get(id__exact=client_id)
                if client is None:
                    redirect('clients')
                if request.is_ajax():
                    response_data = {'client': serializers.serialize('json', [client, ])}
                    return JsonResponse(response_data, safe=False)
                else:
                    # redirect to page
                    return render(request, 'enrollment.html', {'client': client})
                return redirect('clients')
            elif request.method == 'POST':
                client_id = int(str(request.POST.get('client_id')))
                client = Client.objects.filter(id=client_id).first()
                # check if user is from enrolling IP
                if client.implementing_partner == request.user.implementingpartneruser.implementing_partner:
                    # process editing user
                    client.implementing_partner = ImplementingPartner.objects.filter(
                        code__exact=str(request.POST.get('implementing_partner', ''))).first()
                    client.first_name = str(request.POST.get('first_name', ''))
                    client.middle_name = str(request.POST.get('middle_name', ''))
                    client.last_name = str(request.POST.get('last_name', ''))
                    client.date_of_birth = str(request.POST.get('date_of_birth', datetime.now))
                    client.is_date_of_birth_estimated = bool(str(request.POST.get('is_date_of_birth_estimated')))
                    client.verification_document = VerificationDocument.objects.filter(
                        code__exact=str(request.POST.get('verification_document', ''))).first()
                    client.verification_doc_no = str(request.POST.get('verification_doc_no', ''))
                    client.date_of_enrollment = str(request.POST.get('date_of_enrollment', datetime.now))
                    client.age_at_enrollment = int(str(request.POST.get('age_at_enrollment')))
                    client.marital_status = MaritalStatus.objects.filter(code__exact=str(request.POST.get('marital_status', ''))).first()
                    client.phone_number = str(request.POST.get('phone_number', ''))
                    client.dss_id_number = str(request.POST.get('dss_id_number', ''))
                    client.county_of_residence = County.objects.filter(code__exact=request.POST.get('county_of_residence', '')).first()
                    client.sub_county = SubCounty.objects.filter(code__exact=request.POST.get('sub_county', '')).first()
                    client.ward = Ward.objects.filter(code__exact=request.POST.get('ward', 0)).first()
                    client.informal_settlement = str(request.POST.get('informal_settlement', ''))
                    client.village = str(request.POST.get('village', ''))
                    client.landmark = str(request.POST.get('landmark', ''))
                    client.dreams_id = str(request.POST.get('dreams_id', ''))
                    client.guardian_name = str(request.POST.get('guardian_name', ''))
                    client.relationship_with_guardian = str(request.POST.get('relationship_with_guardian', ''))
                    client.guardian_phone_number = str(request.POST.get('guardian_phone_number', ''))
                    client.guardian_national_id = str(request.POST.get('guardian_national_id', ''))
                    client.save(user_id=request.user.id, action="UPDATE")
                    if request.is_ajax():
                        response_data = {
                            'status': 'success',
                            'message': 'Client Details Updated successfuly.',
                            'client_id': client.id
                        }
                        return JsonResponse(json.dumps(response_data), safe=False)
                    else:
                        # redirect to page
                        return redirect('clients')
                else:
                    # user and client IPs dont match. Return error message
                    response_data = {
                        'status': 'failed',
                        'message': 'Operation not allowed. Client is not enrolled by your Implementing partner',
                        'client_id': client.id
                    }
                    return JsonResponse(json.dumps(response_data), safe=False)
        else:
            return PermissionDenied('Operation not allowed. [Missing Permission]')
    except Exception as e:
        tb = traceback.format_exc()
        return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception


def delete_client(request):
    try:
        if request.user is not None and request.user.is_authenticated():
            if request.method == 'GET' and request.is_ajax():
                client_id = int(request.GET['client_id'])
                client = Client.objects.filter(id__exact=client_id).first()
                # check if client and user IPs match
                if client.implementing_partner == request.user.implementingpartneruser.implementing_partner:
                    # check if client has interventions
                    if Intervention.objects.filter(client=client).count() > 0:
                        # Upating audit log
                        log_custom_actions(request.user.id, "DreamsApp_client", client_id, "DELETE", 'FAILED')
                        response_data = {
                            'status': 'fail',
                            'message': 'This client cannot be deleted because they have interventions.'
                        }
                    else:
                        client.delete()
                        # Upating audit log
                        log_custom_actions(request.user.id, "DreamsApp_client", client_id, "DELETE", 'SUCCESS')
                        response_data = {
                            'status': 'success',
                            'message': 'Client Details Deleted successfuly.'
                        }

                else:
                    response_data = {
                        'status': 'failed',
                        'message': 'Operation not allowed. Client is not enrolled by your Implementing partner',
                        'client_id': client.id
                    }
                    # client and user IPs do not match
                return JsonResponse(json.dumps(response_data), safe=False)
            elif request.method == 'POST':
                return PermissionDenied('Operation not allowed. [Missing Permission]')

        else:
            return PermissionDenied('Operation not allowed. [Missing Permission]')
    except Exception as e:
        tb = traceback.format_exc()
        return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception


def testajax(request):
    return render(request, 'testAjax.html')

# Use /ivgetTypes/ in the post url to access the method
# Handles post request for intervention types.
# Receives category_code from request and searches for types in the database


def get_intervention_types(request):

    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        response_data = {}
        category_code = request.POST.get('category_code')

        # Get category by code and gets all related types
        # Returns an object with itypes property
        i_category = InterventionCategory.objects.get(code__exact=category_code)
        i_types = InterventionType.objects.filter(intervention_category__exact=i_category.id)
        i_types = serializers.serialize('json', i_types)
        response_data["itypes"] = i_types
        return JsonResponse(response_data)

    else:
        return HttpResponse("You issued bad request")

# use /ivSave/ to post to the method
# Gets intervention_type_id,  from request


def save_intervention(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        intervention_type_code = int(request.POST.get('intervention_type_code'))
        if intervention_type_code is not None and type(intervention_type_code) is int:
            try:
                i_type = InterventionType.objects.get(code__exact=intervention_type_code)
                intervention = Intervention()
                intervention.client = Client.objects.get(id__exact=int(request.POST.get('client')))
                intervention.intervention_type = i_type
                intervention.intervention_date = request.POST.get('intervention_date')
                created_by = User.objects.get(id__exact=int(request.POST.get('created_by')))
                intervention.created_by = created_by
                intervention.date_created = datetime.now()
                intervention.comment = request.POST.get('comment')

                if i_type.has_hts_result:
                    intervention.hts_result = HTSResult.objects.get(code__exact=int(request.POST.get('hts_result')))

                if i_type.has_pregnancy_result:
                    intervention.pregnancy_test_result = PregnancyTestResult.objects.get(code__exact=int(request.POST.get('pregnancy_test_result')))

                if i_type.has_ccc_number:
                    intervention.client_ccc_number = request.POST.get('client_ccc_number')

                if i_type.has_no_of_sessions:
                    intervention.no_of_sessions_attended = request.POST.get('no_of_sessions_attended')

                # Update implementing Partner
                intervention.implementing_partner = ImplementingPartner.objects.get(id__exact=created_by.implementingpartneruser.implementing_partner.id)
                intervention.save(user_id=request.user.id, action="INSERT")
                # using defer() miraculously solved serialization problem of datetime properties.
                intervention = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created').get(id__exact=intervention.id)

                response_data = {
                    'status': 'success',
                    'message': 'Intervention successfully saved',
                    'intervention': serializers.serialize('json', [intervention, ], ensure_ascii=False),
                    'i_type': serializers.serialize('json', [i_type])
                }

                return JsonResponse(response_data)
            except Exception as e:
                tb = traceback.format_exc()
                return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception
        else:
            return HttpResponseServerError('Invalid Intervention Type')
    else:
        return PermissionDenied('Operation not allowed. [Missing Permission]')

# method that returns a list of interventions of given category for a given client
# use /ivList/ url pattern to access the method


def get_intervention_list(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        if 'client_id' not in request.POST or request.POST.get('client_id') == 0:
            return ValueError('No Client id found in your request! Ensure it is provided')
        if 'intervention_category_code' not in request.POST or request.POST.get('intervention_category_code') == 0:
            return ValueError('No Intervention Category Code found in your request! Ensure it is provided')

        client_id = request.POST.get('client_id')
        intervention_category_code = request.POST.get('intervention_category_code')
        try:
            iv_category = InterventionCategory.objects.get(code__exact=intervention_category_code)
            list_of_related_iv_types = InterventionType.objects.filter(intervention_category__exact=iv_category)
            iv_type_ids = [i_type.id for i_type in list_of_related_iv_types]
            # check for see_other_ip_data persmission

            list_of_interventions = Intervention.objects.defer('date_changed', 'intervention_date',
                                                               'date_created').filter(client__exact=client_id,
                                                                                      intervention_type__in=iv_type_ids)
            if not request.user.has_perm('auth.can_view_other_ip_data'):
                list_of_interventions = list_of_interventions.filter(implementing_partner_id=request.user.implementingpartneruser.implementing_partner.id)

            if not request.user.has_perm('auth.can_view_records_older_than_a_week'):
                list_of_interventions = list_of_interventions.filter(date_created__range=
                                                                     [datetime.now() - timedelta(days=7),
                                                                      datetime.now()]
                                                                     )
            response_data = {
                'iv_types': serializers.serialize('json', list_of_related_iv_types),
                'interventions': serializers.serialize('json', list_of_interventions)
            }
            return JsonResponse(response_data)
        except ObjectDoesNotExist as nf:
            return ObjectDoesNotExist(traceback.format_exc())
        except Exception as e:
            return HttpResponseServerError(traceback.format_exc())
    else:
        return PermissionDenied('Missing permissions')

# Gets an intervention. Takes intervention_id and returns Intervention object
# use /ivGet/ to access this method


def get_intervention(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        intervention_id = request.POST.get('intervention_id')
        if 'intervention_id' not in request.POST:
            return ValueError('No intervention id found in your request!')
        try:
            intervention = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created').get(id__exact=intervention_id)
            if intervention is not None:
                response_data = {'intervention': serializers.serialize('json', [intervention, ])}
                return JsonResponse(response_data)
            else:
                return ObjectDoesNotExist('No Intervention with the provided Id')
        except Exception as e:
            return HttpResponseServerError(traceback.format_exc())

    else:
        return PermissionDenied('Operation not allowed. [Missing permission]')


# Updates an intervention
# use /ivUpdate/ to access the method


def update_intervention(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        intervention_id = int(request.POST.get('intervention_id'))
        if intervention_id is not None and type(intervention_id) is int:
            try:
                intervention = Intervention.objects.get(id__exact=intervention_id)
                # check if intervention belongs to the ip
                if intervention.implementing_partner == request.user.implementingpartneruser.implementing_partner:
                    intervention.client = Client.objects.get(id__exact=int(request.POST.get('client')))
                    intervention.intervention_date = request.POST.get('intervention_date')
                    intervention.changed_by = User.objects.get(id__exact=int(request.POST.get('changed_by')))
                    intervention.date_changed = datetime.now()
                    intervention.comment = request.POST.get('comment')

                    i_type = InterventionType.objects.get(id__exact=intervention.intervention_type.id)

                    if i_type.has_hts_result:
                        intervention.hts_result = HTSResult.objects.get(code__exact=int(request.POST.get('hts_result')))

                    if i_type.has_pregnancy_result:
                        intervention.pregnancy_test_result = PregnancyTestResult.objects.get(code__exact=int(request.POST.get('pregnancy_test_result')))

                    if i_type.has_ccc_number:
                        intervention.client_ccc_number = request.POST.get('client_ccc_number')

                    if i_type.has_no_of_sessions:
                        intervention.no_of_sessions_attended = request.POST.get('no_of_sessions_attended')


                    intervention.save(user_id=request.user.id, action="UPDATE")
                    # using defer() miraculously solved serialization problem of datetime properties.
                    intervention = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created').get(id__exact=intervention.id)
                    # construct response

                    response_data = {
                        'status': 'success',
                        'message': 'Intervention successfully updated',
                        'intervention': serializers.serialize('json', [intervention, ], ensure_ascii=False),
                        'i_type': serializers.serialize('json', [i_type])
                    }
                else:
                    # Intervention does not belong to Implementing partner. Send back error message
                    response_data = {
                        'status': 'failed',
                        'message': 'You do not have the rights to update this intervention because it was created by a '
                                   'different Implementing Partner'
                    }
                return JsonResponse(response_data)
            except Exception as e:
                tb = traceback.format_exc()
                return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception
        else:
            return HttpResponseServerError('Invalid Intervention Type')
    else:
        return PermissionDenied('Operation not allowed. [Missing Permission]')


def delete_intervention(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        intervention_id = int(request.POST.get('intervention_delete_id'))
        if intervention_id is not None and type(intervention_id) is int:
            try:
                # get intervention
                # Check if intervention belongs to IP
                intervention = Intervention.objects.filter(pk=intervention_id).first()
                if intervention.implementing_partner == request.user.implementingpartneruser.implementing_partner:
                    intervention.delete()
                    log_custom_actions(request.user.id, "DreamsApp_intervention", intervention_id, "DELETE", None)
                    response_data = {
                        'result': 'success',
                        'message': 'Intervention has been successfully deleted',
                        'intervention_id': intervention_id
                    }
                else:
                    # Intervention does not belong to IP
                    log_custom_actions(request.user.id, "DreamsApp_intervention", intervention_id, "DELETE", "Failed attempt")
                    response_data = {
                        'result': 'failed',
                        'message': 'You do not have the rights to delete this intervention because it was created by a '
                                   'different Implementing Partner',
                        'intervention_id': intervention_id
                    }
                return JsonResponse(json.dumps(response_data), safe=False)
            except Exception as e:
                tb = traceback.format_exc()
                return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception
        else:
            return HttpResponseServerError('Invalid Intervention Type')
    else:
        return PermissionDenied('Operation not allowed. [Missing Permission]')


def get_sub_counties(request):

    if request.method == 'GET' and request.user is not None and request.user.is_authenticated():
        response_data = {}
        county_code = request.GET['county_code']

        county = County.objects.get(code__exact=county_code)
        sub_counties = SubCounty.objects.filter(county__exact=county.id)
        sub_counties = serializers.serialize('json', sub_counties)
        response_data["sub_counties"] = sub_counties
        return JsonResponse(response_data)

    else:
        return HttpResponse("You issued bad request")


def get_wards(request):

    if request.method == 'GET' and request.user is not None and request.user.is_authenticated():
        response_data = {}
        sub_county_code = request.GET['sub_county_code']

        sub_county = SubCounty.objects.get(code__exact=sub_county_code)
        wards = Ward.objects.filter(sub_county__exact=sub_county.id)
        wards = serializers.serialize('json', wards)
        response_data["wards"] = wards
        return JsonResponse(response_data)

    else:
        return HttpResponse("You issued bad request")


def log_me_out(request):
    logout(request)
    return redirect('login')


def reporting(request):
    try:
        if request.user is not None and request.user.is_authenticated():
            if request.method == 'GET':
                return render(request, 'reporting.html', {'user': request.user})
            elif request.method == 'POST' and request.is_ajax():
                return render(request, 'reporting.html', {'user': request.user})
        else:
            return PermissionDenied('Operation not allowed. [Missing Permission]')
    except Exception as e:
        tb = traceback.format_exc()
        return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception


def user_help(request):
    try:
        if request.user is not None and request.user.is_authenticated():
            if request.method == 'GET':
                return render(request, 'help.html', {'user': request.user})
            elif request.method == 'POST' and request.is_ajax():
                return render(request, 'help.html', {'user': request.user})
        else:
            return PermissionDenied('Operation not allowed. [Missing Permission]')
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception


def logs(request):
    if request.user.is_authenticated():
        if not request.user.has_perm('auth.can_view_logs'):
            return PermissionDenied('Operation not allowed. [Missing Permission]')
        # user is allowed to view logs
        if request.method == 'GET':
            try:
                page = request.GET.get('page', 1)
                filter_text = request.GET.get('filter-log-text', '')
                filter_date = request.GET.get('filter-log-date', '')
                # getting logs
                if filter_date == '':
                    logs = Audit.objects.filter(Q(table__contains=filter_text) |
                                                Q(action__contains=filter_text) |
                                                Q(search_text__contains=filter_text)
                                                ).order_by('-timestamp')
                else:
                    yr, mnth, dt = filter_date.split('-')
                    constructed_date = date(int(yr), int(mnth), int(dt))
                    logs = Audit.objects.filter((Q(table__contains=filter_text) |
                                                 Q(action__contains=filter_text) |
                                                 Q(search_text__contains=filter_text)) &
                                                Q(timestamp__year=constructed_date.year,
                                                  timestamp__month=constructed_date.month,
                                                  timestamp__day=constructed_date.day)
                                                ).order_by('-timestamp')
                paginator = Paginator(logs, 25)  # Showing 25 contacts per page
                try:
                    logs_list = paginator.page(page)
                except PageNotAnInteger:
                    logs_list = paginator.page(1)  # Deliver the first page is page is not an integer
                except EmptyPage:
                    logs_list = paginator.page(0)  # Deliver the last page if page is out of scope
                return render(request, 'log.html', {'page': 'logs', 'logs': logs_list, 'filter_text': filter_text,
                                                    'filter_date': filter_date
                                                    }
                              )
            except Exception as e:
                tb = traceback.format_exc(e)
                return HttpResponseServerError(tb)
        elif request.method == 'POST':
            # get the form data
            filter_text = request.POST.get('filter-log-text', '')
            filter_date = request.POST.get('filter-log-date', '')
            if filter_date == '':
                logs = Audit.objects.filter(Q(table__contains=filter_text) |
                                            Q(action__contains=filter_text) |
                                            Q(search_text__contains=filter_text)
                                            ).order_by('-timestamp')
            else:
                yr, mnth, dt = filter_date.split('-')
                constructed_date = date(int(yr), int(mnth), int(dt))
                logs = Audit.objects.filter((Q(table__contains=filter_text) |
                                            Q(action__contains=filter_text) |
                                            Q(search_text__contains=filter_text)) &
                                            Q(timestamp__year=constructed_date.year, timestamp__month=constructed_date.month, timestamp__day=constructed_date.day)
                                            )
            paginator = Paginator(logs, 25)
            try:
                logs_list = paginator.page(1)
            except PageNotAnInteger:
                logs_list = paginator.page(1)  # Deliver the first page is page is not an integer
            except EmptyPage:
                logs_list = paginator.page(0)  # Deliver the last page if page is out of scope
            return render(request, 'log.html', {'page': 'logs', 'logs': logs_list, 'filter_text': filter_text,
                                                'filter_date': filter_date})
    else:
        # user is not allowed to view logs redirect to clients page with a message
        return redirect('clients')


def upload_dreams_excel_database(request):

    if request.method == 'POST':
        form = EnrollmentDocumentUpload(request.POST, request.FILES)
        if form.is_valid():
            dreams_doc = request.FILES['docfile']

            excel_db = DreamsEnrollmentExcelDatabase()
            excel_db.create_tmp_file(dreams_doc)
            tmp_file_path = excel_db.document_path
            if tmp_file_path is not None:

                excel_db.excel_enrollment_data()
            else:
                print 'Temp file not created'

            return render(request, 'excel_upload_progress.html')
    else:
        form = EnrollmentDocumentUpload()
        return render(request, 'excel_db_upload.html', {'form': form})

