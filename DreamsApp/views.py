# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseServerError
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.exceptions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.views.generic import ListView, CreateView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.forms.models import model_to_dict
import json
import traceback
from datetime import date, timedelta
from django.db.models import Q
from DreamsApp.models import *
from DreamsApp.forms import *

def get_enrollment_form_config_data():
    try:
        config_data = {
            'implementing_partners': ImplementingPartner.objects.all(),
            'verification_documents': VerificationDocument.objects.all(),
            'marital_status': MaritalStatus.objects.all(),
            'counties': County.objects.all()
            #  'sub_counties': SubCounty.objects.all(),
            #  'wards': Ward.objects.all()
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
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def clients(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'GET':
                client_list = Client.objects.filter(id__exact=0)  # Clients list should be empty on start
                implementing_partner_user = ImplementingPartnerUser.objects.filter(user=request.user).first()
                context = {'page': 'clients', 'user': request.user, 'clients': client_list,
                           'implementing_partner_user': implementing_partner_user,
                           'config_data': get_enrollment_form_config_data()}
                return render(request, 'clients.html', context)
            elif request.method == 'POST':
                search_value = request.POST.get('searchValue', '')

                if request.user.has_perm('auth.can_search_client_by_name'):
                    search_result = Client.objects.filter(Q(dreams_id__in=search_value.split(" ")) |
                                                          Q(first_name__in=search_value.split(" ")) |
                                                          Q(last_name__in=search_value.split(" ")) |
                                                          Q(middle_name__in=search_value.split(" "))).first()
                else:
                    search_result = Client.objects.filter(dreams_id__exact=search_value).first()
                # check if user can see clients enrolled more than a week ago
                log_custom_actions(request.user.id, "DreamsApp_client", None, "SEARCH", search_value)
                json_response = {
                    'search_result': serializers.serialize('json', [search_result]),
                    'can_manage_client': request.user.has_perm('auth.can_manage_client'),
                    'can_change_client': request.user.has_perm('auth.can_change_client'),
                    'can_delete_client': request.user.has_perm('auth.can_delete_client')
                }
                return JsonResponse(json_response, safe=False)
        else:
            return redirect('login')
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def client_profile(request):
    """ Returns client profile """
    if request.user is not None and request.user.is_authenticated() and request.user.is_active:
        if request.method == 'GET':
            client_id = int(request.GET['client_id'])
        else:
            client_id = int(request.POST('client_id', ''))

        if client_id is not None and client_id != 0:
            try:
                client_found = Client.objects.get(id=client_id)
                if client_found is not None:
                    # get cash transfer details
                    cash_transfer_details = ClientCashTransferDetails.objects.get(client=client_found)
                    # create cash transfer details form
                    cash_transfer_details_form = ClientCashTransferDetailsForm(instance=cash_transfer_details,
                                                                               current_AGYW=client_found)
                    cash_transfer_details_form.save(commit=False)
                return render(request, 'client_profile.html', {'page': 'clients',
                                                               'client': client_found,
                                                               'ct_form': cash_transfer_details_form,
                                                               'ct_id': cash_transfer_details.id,
                                                               'user': request.user
                                                               })
            except ClientCashTransferDetails.DoesNotExist:
                cash_transfer_details_form = ClientCashTransferDetailsForm(current_AGYW=client_found)
                return render(request, 'client_profile.html',
                              {'page': 'clients',
                               'client': client_found,
                               'ct_form': cash_transfer_details_form,
                               'user': request.user
                               })
            except Client.DoesNotExist:
                return render(request, 'login.html')
            except Exception as e:
                return render(request, 'login.html')
    else:
        raise PermissionDenied


def save_client(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
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
                    marital_status=MaritalStatus.objects.filter(
                        code__exact=str(request.POST.get('marital_status', ''))).first(),
                    phone_number=request.POST.get('phone_number', ''),
                    dss_id_number=request.POST.get('dss_id_number', ''),
                    county_of_residence=County.objects.filter(
                        code__exact=request.POST.get('county_of_residence', '')).first(),
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
                        'client_id': client.id,
                        'can_manage_client': request.user.has_perm('auth.can_manage_client'),
                        'can_change_client': request.user.has_perm('auth.can_change_client'),
                        'can_delete_client': request.user.has_perm('auth.can_delete_client')
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


def edit_client(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:  # and request.user.is_superuser:
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
                    client.marital_status = MaritalStatus.objects.filter(
                        code__exact=str(request.POST.get('marital_status', ''))).first()
                    client.phone_number = str(request.POST.get('phone_number', ''))
                    client.dss_id_number = str(request.POST.get('dss_id_number', ''))
                    client.county_of_residence = County.objects.filter(
                        code__exact=request.POST.get('county_of_residence', '')).first()
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
                            'client_id': client.id,
                            'can_manage_client': request.user.has_perm('auth.can_manage_client'),
                            'can_change_client': request.user.has_perm('auth.can_change_client'),
                            'can_delete_client': request.user.has_perm('auth.can_delete_client')
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
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def delete_client(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
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
                return JsonResponse(json.dumps(response_data), safe=False)
            elif request.method == 'POST':
                raise PermissionDenied
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


def testajax(request):
    return render(request, 'testAjax.html')


# Use /ivgetTypes/ in the post url to access the method
# Handles post request for intervention types.
# Receives category_code from request and searches for types in the database


def get_intervention_types(request):
    try:
        if request.method == 'POST' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
            response_data = {}
            category_code = request.POST.get('category_code')
            current_client_id = request.POST.get('current_client_id', 0)
            # get current client
            current_client = Client.objects.filter(id__exact=current_client_id).first()
            if current_client is None:
                raise Exception
            # Get category by code and gets all related types
            # Returns an object with itypes property
            given_intervention_type_ids = Intervention.objects.values_list('intervention_type', flat=True). \
                filter(client=current_client). \
                distinct()  # select distinct intervention type ids given to a user
            i_category = InterventionCategory.objects.get(code__exact=category_code)
            # compute age at enrollment
            current_age = current_client.get_current_age()
            i_types = InterventionType.objects.filter(intervention_category__exact=i_category.id, ) \
                .exclude(is_age_restricted=True, min_age__gt=current_age) \
                .exclude(is_age_restricted=True, max_age__lt=current_age) \
                .exclude(is_given_once=True, id__in=given_intervention_type_ids).order_by('code')
            # get id's of interventions that can only be given once and are already given
            i_types = serializers.serialize('json', i_types)
            response_data["itypes"] = i_types
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
        if request.method == 'POST' and request.user is not None and request.user.is_authenticated() \
                and request.user.is_active:
            # Check if user belongs to an Ip
            if request.user.implementingpartneruser.implementing_partner is not None:
                intervention_type_code = int(request.POST.get('intervention_type_code'))
                if intervention_type_code is not None and type(intervention_type_code) is int:
                    i_type = InterventionType.objects.get(code__exact=intervention_type_code)
                    intervention = Intervention()
                    intervention.client = Client.objects.get(id__exact=int(request.POST.get('client')))
                    intervention.intervention_type = i_type
                    intervention.name_specified = request.POST.get('other_specify', '') if i_type.is_specified else ''
                    intervention.intervention_date = request.POST.get('intervention_date')
                    created_by = User.objects.get(id__exact=int(request.POST.get('created_by')))
                    intervention.created_by = created_by
                    intervention.date_created = datetime.now()
                    intervention.comment = request.POST.get('comment', '')

                    if i_type.has_hts_result:
                        intervention.hts_result = HTSResult.objects.get(code__exact=int(request.POST.get('hts_result')))

                    if i_type.has_pregnancy_result:
                        intervention.pregnancy_test_result = PregnancyTestResult.objects.get(
                            code__exact=int(request.POST.get('pregnancy_test_result')))

                    if i_type.has_ccc_number:
                        intervention.client_ccc_number = request.POST.get('client_ccc_number')

                    if i_type.has_no_of_sessions:
                        intervention.no_of_sessions_attended = request.POST.get('no_of_sessions_attended')

                    # Update implementing Partner
                    intervention.implementing_partner = ImplementingPartner.objects. \
                        get(id__exact=created_by.implementingpartneruser.implementing_partner.id)
                    intervention.save(user_id=request.user.id, action="INSERT")
                    # using defer() miraculously solved serialization problem of datetime properties.
                    intervention = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created'). \
                        get(id__exact=intervention.id)
                    response_data = {
                        'status': 'success',
                        'message': 'Intervention successfully saved',
                        'intervention': serializers.serialize('json', [intervention, ], ensure_ascii=False),
                        'i_type': serializers.serialize('json', [i_type]),
                        'hts_results': serializers.serialize('json', HTSResult.objects.all()),
                        'pregnancy_results': serializers.serialize('json', PregnancyTestResult.objects.all())
                    }
                    return JsonResponse(response_data)
                else:  # Invalid Intervention Type
                    raise Exception("Error: Invalid Intervention Type. "
                                    "Please select a valid Intervention Type to Proceed")
            else:  # User has no valid IP.
                raise Exception("Error: You do not belong to an Implementing Partner. "
                                "Please contact your system admin to add you to the relevant Implementing Partner.")
        else:
            raise PermissionDenied
    except Exception as e:
        # Return error with message
        response_data = {
            'status': 'fail',
            'message': e.message
        }
        return JsonResponse(response_data)


# method that returns a list of interventions of given category for a given client
# use /ivList/ url pattern to access the method


def get_intervention_list(request):
    try:
        if request.method == 'POST' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if 'client_id' not in request.POST or request.POST.get('client_id') == 0:
                return ValueError('No Client id found in your request! Ensure it is provided')
            if 'intervention_category_code' not in request.POST or request.POST.get('intervention_category_code') == 0:
                return ValueError('No Intervention Category Code found in your request! Ensure it is provided')

            client_id = request.POST.get('client_id')
            intervention_category_code = request.POST.get('intervention_category_code')
            iv_category = InterventionCategory.objects.get(code__exact=intervention_category_code)
            list_of_related_iv_types = InterventionType.objects.filter(intervention_category__exact=iv_category)
            iv_type_ids = [i_type.id for i_type in list_of_related_iv_types]
            # check for see_other_ip_data persmission

            list_of_interventions = Intervention.objects.defer('date_changed', 'intervention_date',
                                                               'date_created').filter(client__exact=client_id,
                                                                                      intervention_type__in=iv_type_ids).order_by(
                '-intervention_date', '-date_created', '-date_changed')
            if not request.user.has_perm('auth.can_view_cross_ip_data'):
                list_of_interventions = list_of_interventions.filter(
                    implementing_partner_id=request.user.implementingpartneruser.implementing_partner.id)

            if not request.user.has_perm('auth.can_view_older_records'):
                list_of_interventions = list_of_interventions.filter(date_created__range=
                                                                     [datetime.now() - timedelta(days=31),
                                                                      datetime.now()]
                                                                     )
            response_data = {
                'iv_types': serializers.serialize('json', list_of_related_iv_types),
                'interventions': serializers.serialize('json', list_of_interventions),
                'hts_results': serializers.serialize('json', HTSResult.objects.all()),
                'pregnancy_results': serializers.serialize('json', PregnancyTestResult.objects.all())
            }
            return JsonResponse(response_data)
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)


# Gets an intervention. Takes intervention_id and returns Intervention object
# use /ivGet/ to access this method


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


# Updates an intervention
# use /ivUpdate/ to access the method


def update_intervention(request):
    try:
        if request.method == 'POST' and request.user is not None and request.user.is_authenticated() and \
                request.user.is_active:
            # Check if user belongs to an Ip
            if request.user.implementingpartneruser.implementing_partner is not None:
                intervention_id = int(request.POST.get('intervention_id'))
                if intervention_id is not None and type(intervention_id) is int:
                    intervention = Intervention.objects.get(id__exact=intervention_id)
                    # check if intervention belongs to the ip
                    if intervention.implementing_partner == request.user.implementingpartneruser.implementing_partner:
                        intervention.client = Client.objects.get(id__exact=int(request.POST.get('client')))
                        intervention.name_specified = request.POST.get('other_specify',
                                                                       '') if intervention.intervention_type.is_specified else ''
                        intervention.intervention_date = request.POST.get('intervention_date')
                        intervention.changed_by = User.objects.get(id__exact=int(request.POST.get('changed_by')))
                        intervention.date_changed = datetime.now()
                        intervention.comment = request.POST.get('comment')

                        i_type = InterventionType.objects.get(id__exact=intervention.intervention_type.id)

                        if i_type.has_hts_result:
                            intervention.hts_result = HTSResult.objects.get(
                                code__exact=int(request.POST.get('hts_result')))

                        if i_type.has_pregnancy_result:
                            intervention.pregnancy_test_result = PregnancyTestResult.objects.get(
                                code__exact=int(request.POST.get('pregnancy_test_result')))

                        if i_type.has_ccc_number:
                            intervention.client_ccc_number = request.POST.get('client_ccc_number')

                        if i_type.has_no_of_sessions:
                            intervention.no_of_sessions_attended = request.POST.get('no_of_sessions_attended')

                        intervention.save(user_id=request.user.id, action="UPDATE")
                        # using defer() miraculously solved serialization problem of datetime properties.
                        intervention = Intervention.objects.defer('date_changed', 'intervention_date',
                                                                  'date_created').get(id__exact=intervention.id)
                        # construct response

                        response_data = {
                            'status': 'success',
                            'message': 'Intervention successfully updated',
                            'intervention': serializers.serialize('json', [intervention, ], ensure_ascii=False),
                            'i_type': serializers.serialize('json', [i_type]),
                            'hts_results': serializers.serialize('json', HTSResult.objects.all()),
                            'pregnancy_results': serializers.serialize('json', PregnancyTestResult.objects.all())
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
            raise PermissionDenied
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': e.message
        }
        return JsonResponse(response_data)


def delete_intervention(request):
    try:
        if request.method == 'POST' and request.user is not None and request.user.is_authenticated() and \
                request.user.is_active:
            # Check if user belongs to an Ip
            if request.user.implementingpartneruser.implementing_partner is not None:
                intervention_id = int(request.POST.get('intervention_delete_id'))
                if intervention_id is not None and type(intervention_id) is int:
                    # get intervention
                    # Check if intervention belongs to IP
                    intervention = Intervention.objects.filter(pk=intervention_id).first()
                    if intervention.implementing_partner == request.user.implementingpartneruser.implementing_partner:
                        intervention.delete()
                        log_custom_actions(request.user.id, "DreamsApp_intervention", intervention_id, "DELETE", None)
                        response_data = {
                            'status': 'success',
                            'message': 'Intervention has been successfully deleted',
                            'intervention_id': intervention_id
                        }
                        return JsonResponse(response_data)
                    else:
                        raise Exception(
                            'You do not have the rights to delete this intervention because it was created by a '
                            'different Implementing Partner'
                        )
                else:
                    raise Exception("Error: No intervention selected for deletion")
            else:
                raise Exception("Error: You do not belong to an Implementing Partner. "
                                "Please contact your system admin to add you to the relevant Implementing Partner.")
        else:
            raise PermissionDenied
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': e.message
        }
        return JsonResponse(response_data)


def get_sub_counties(request):
    try:
        if request.method == 'GET' and request.user is not None and request.user.is_authenticated() and request.user.is_active:
            response_data = {}
            county_code = request.GET['county_code']
            county = County.objects.get(code__exact=county_code)
            sub_counties = SubCounty.objects.filter(county__exact=county.id)
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
        sub_county_code = request.GET['sub_county_code']
        sub_county = SubCounty.objects.get(code__exact=sub_county_code)
        wards = Ward.objects.filter(sub_county__exact=sub_county.id)
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
                return render(request, 'reporting.html', {'user': request.user})
            elif request.method == 'POST' and request.is_ajax():
                return render(request, 'reporting.html', {'user': request.user})
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc()
        return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception


def user_help(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'GET':
                return render(request, 'help.html', {'user': request.user})
            elif request.method == 'POST' and request.is_ajax():
                return render(request, 'help.html', {'user': request.user})
        else:
            raise PermissionDenied
    except Exception as e:
        tb = traceback.format_exc(e)
        return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception


def logs(request):
    if request.user.is_authenticated() and request.user.is_active:
        if not request.user.has_perm('auth.can_manage_audit'):
            raise PermissionDenied('Operation not allowed. [Missing Permission]')
        # user is allowed to view logs
        if request.method == 'GET':
            try:
                page = request.GET.get('page', 1)
                filter_text = request.GET.get('filter-log-text', '')
                filter_date = request.GET.get('filter-log-date', '')
                # getting logs
                if filter_date == '':
                    logs = Audit.objects.filter(Q(table__in=filter_text.split(" ")) |
                                                Q(action__in=filter_text.split(" ")) |
                                                Q(search_text__in=filter_text.split(" "))
                                                ).order_by('-timestamp')
                else:
                    yr, mnth, dt = filter_date.split('-')
                    constructed_date = date(int(yr), int(mnth), int(dt))
                    logs = Audit.objects.filter((Q(table__in=filter_text.split(" ")) |
                                                 Q(action__in=filter_text.split(" ")) |
                                                 Q(search_text__in=filter_text.split(" "))) &
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
                                                    'filter_date': filter_date,
                                                    'items_in_page': 0 if logs_list.end_index() == 0 else
                                                    (logs_list.end_index() - logs_list.start_index() + 1)
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
                                            Q(timestamp__year=constructed_date.year,
                                              timestamp__month=constructed_date.month,
                                              timestamp__day=constructed_date.day)
                                            )
            paginator = Paginator(logs, 25)
            try:
                logs_list = paginator.page(1)
            except PageNotAnInteger:
                logs_list = paginator.page(1)  # Deliver the first page is page is not an integer
            except EmptyPage:
                logs_list = paginator.page(0)  # Deliver the last page if page is out of scope
            return render(request, 'log.html', {'page': 'logs', 'logs': logs_list, 'filter_text': filter_text,
                                                'filter_date': filter_date,
                                                'items_in_page': 0 if logs_list.end_index() == 0 else
                                                (logs_list.end_index() - logs_list.start_index() + 1)})
    else:
        raise PermissionDenied


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
            if not request.user.has_perm('auth.can_view_cross_ip_data'):
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
        return render(request, 'users.html', {'page': 'users', 'ip_users': final_ip_user_list,
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
                request.POST.get('implementing_partner', ''))  # Valid IP for new user
            # check if user can change cross IP data
            if not request.user.has_perm('auth.can_change_cross_ip_data'):
                # User must register new user under their IP. Theck if user has a valid IP
                # check if registering user belongs to an IP
                if request.user.implementingpartneruser.implementing_partner is None: # Registering user does not belong to an IP. Raise exception
                    raise Exception("Error: You do not belong to an Implementing Partner. "
                                    "Please contact your system admin to add you to the relevant Implementing Partner.")

                elif new_user_ip != request.user.implementingpartneruser.implementing_partner:
                    # Registering user and user do not belong to same IP. Raise exception
                    raise Exception("Error: You do not have permission to register a user under a different Implementing"
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
                                        'Contact System Admin for help ' + e.message,
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
                'message': e.message,
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
                                            'Please contact system admin for assistance')
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
            'message': e.message
        }
        return JsonResponse(response_data)


def change_cred(request):
    # check if user is logged in
    if request.user.is_authenticated() and request.user.is_active:  # user is authenticated
        if request.method == 'GET':
            # return password change view
            context = {'page': 'users', 'user': request.user,}
            return render(request, 'change_cred.html', context)
        elif request.method == 'POST':
            # do post functionality here!!
            # retrieve all fields
            ch_username = request.POST.get('ch_username', '')
            ch_current_password = request.POST.get('ch_current_password', '')
            ch_new_password = request.POST.get('ch_new_password', '')
            ch_confirm_new_password = request.POST.get('ch_confirm_new_password', '')
            # check if any details is missing
            if ch_username == '' or ch_current_password == '' or ch_new_password == '' or ch_confirm_new_password == '' or ch_confirm_new_password == '':
                # return error
                response_data = {
                    'status': 'fail',
                    'message': 'An error occurred as a result of missing details.'
                }
                return JsonResponse(response_data)
            else:
                # all details exist. Check if credentials match
                # check username
                if request.user.get_username() == ch_username and request.user.check_password(
                        ch_current_password) and ch_new_password == ch_confirm_new_password:
                    # all details match. Change user password
                    request.user.set_password(ch_new_password)
                    request.user.save()
                    # return success message
                    response_data = {
                        'status': 'success',
                        'message': 'Password changed successfully. Proceed to login with your new credentials'
                    }
                    return JsonResponse(response_data)

                else:
                    # username or password mismatch. return error message
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
                   'Your browser sent a request that this server could not understand<br>. '}
    return render(request, 'error_page.html', context)


def permission_denied(request):  # PermissionDenied('Operation not allowed. [Missing Permission]')
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
                   'administrator if the error persists.<br>. '}
    return render(request, 'error_page.html', context)


def grievances_list(request):
    try:
        if not request.user.is_authenticated():
            raise PermissionDenied
        page = request.GET.get('page', 1) if request.method == 'GET' else request.POST.get('page', 1)
        filter_date = request.GET.get('filter_date', None) if request.method == 'GET' else request.POST.get('filter_date', None)
        filter_text = request.GET.get('filter-user-text', '') if request.method == 'GET' else request.POST.get('filter-user-text', '')
        """ IP level permission check """
        grievance_list = Grievance.objects.all() if request.user.has_perm('auth.can_view_cross_ip') else \
            Grievance.objects.filter(implementing_partner=request.user.implementingpartneruser.implementing_partner)
        """Date filter """
        if filter_date is not None and filter_date is not u'':
            yr, mnth, dt = filter_date.split('-')
            constructed_date = date(int(yr), int(mnth), int(dt))
            grievance_list = Grievance.objects.filter(Q(date__year=constructed_date.year,
                                                        date__month=constructed_date.month,
                                                        date__day=constructed_date.day))
        """ Text filter """
        #if filter_text is not u'' and filter_text is not '':
            #grievance_list = Grievance.objects.filter(Q(reporter_name__contains=filter_text) |
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
            'page': 'cash_transfer',
            'filter_text': filter_text,
            'filter_date': filter_date,
            'items_in_page': 0 if final_grievance_list.end_index() == 0 else
            (final_grievance_list.end_index() - final_grievance_list.start_index() + 1),
            'current_user_ip': request.user.implementingpartneruser.implementing_partner,
            'form': GrievanceModelForm(current_user=request.user),
            'grievance_list': final_grievance_list,
            'status': 'success'
        }
        return render(request, 'grievances.html', response_data)
    except Exception as e:
        response_data = {
            'status': 'fail',
            'message': e.message
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
            'message': e.message
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
            'message': e.message
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
            'message': e.message
        }
        return JsonResponse(response_data)


def grievances_get(request):
    """ """
    try:
        if not request.user.is_authenticated():
            raise PermissionDenied
        grievance_id = request.GET.get('grievance_id', 0) if request.method == 'GET' else request.POST.get('grievance_id', 0)
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
            'message': e.message
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
            'message': e.message
        }
        return JsonResponse(response_data)

