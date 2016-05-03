from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
import traceback
from django.core.exceptions import *
from django.core import serializers
from django.contrib.auth import login, logout
import json

from django.contrib.auth import authenticate
from django.db.models import Q
from DreamsApp.models import *


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        user_name = request.POST.get('inputUsername', '')
        pass_word = request.POST.get('inputPassword', '')
        if user_name == '' or pass_word == '':
            return render(request, 'index.html')
        else:
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('clients')
                else:
                    return HttpResponse("Login Successful, but the account has been disabled!")
            else:
                return HttpResponse('Login Failed')
    else:
        return render(request, 'index.html')


def clients(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            if request.method == 'GET':
                client_list = Client.objects.all()   # filter to get patients only. Not yet done
                context = {'user': request.user, 'clients': client_list}
                return render(request, 'clients.html', context)
            elif request.method == 'POST' and request.is_ajax():
                search_value = request.POST.get('searchValue', '')
                search_result = Client.objects.filter(Q(first_name__startswith=search_value) |
                                                      Q(last_name__startswith=search_value) |
                                                      Q(middle_name__startswith=search_value))
                return JsonResponse(serializers.serialize('json', search_result), safe=False)
            elif request.method == 'POST':
                search_value = request.POST.get('searchValue', '')
                search_result = Client.objects.filter(Q(first_name__startswith=search_value) |
                                                      Q(last_name__startswith=search_value) |
                                                      Q(middle_name__startswith=search_value))
                return JsonResponse(serializers.serialize('json', search_result), safe=False)
        else:
            return redirect('index')
    except Exception as e:
        return redirect('index')


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
                    return render(request, 'client_profile.html', {'client': client_found, 'user': request.user})
            except:
                return render(request, 'index.html')
    return render(request, 'index.html')


def save_client(request):
    try:
        if request.user is not None and request.user.is_authenticated():
            if request.method == 'GET':
                return render(request, 'enrollment.html', {'client': None})
            elif request.method == 'POST' and request.is_ajax():
                # process saving user
                Client.objects.create(
                    first_name=request.POST.get('first_name', ''),
                    middle_name=request.POST.get('middle_name', ''),
                    last_name=request.POST.get('last_name', ''),
                    date_of_birth=request.POST.get('date_of_birth', ''),
                    is_date_of_birth_estimated=request.POST.get('is_date_of_birth_estimated', ''),
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
                if request.is_ajax():
                    response_data = {
                        'status': 'success',
                        'message': 'Enrollment to DREAMS successful.'
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
        if request.user is not None and request.user.is_authenticated():
            if request.method == 'GET':
                client_id = int(request.GET['client_id'])
                client = Client.objects.defer('date_of_birth', 'date_of_enrollment').get(id__exact=client_id)
                if client is None:
                    redirect('clients')
                return render(request, 'enrollment.html', {'client': client})
            elif request.method == 'POST':
                client_id = int(str(request.POST.get('client_id')))
                client = Client.objects.filter(id=client_id).first()
                # process editing user
                client.first_name = str(request.POST.get('first_name', ''))
                client.middle_name = str(request.POST.get('middle_name', ''))
                client.last_name = str(request.POST.get('last_name', ''))
                client.date_of_birth = str(request.POST.get('date_of_birth', datetime.now))
                client.is_date_of_birth_estimated = bool(str(request.POST.get('is_date_of_birth_estimated')))
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
                client.save()
                if request.is_ajax():
                    response_data = {
                        'status': 'success',
                        'message': 'Client Details Updated successfuly.'
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


def delete_client(request):
    try:
        if request.user is not None and request.user.is_authenticated():
            if request.method == 'GET' and request.is_ajax():
                client_id = int(request.GET['client_id'])
                client = Client.objects.filter(id__exact=client_id).first()
                client.delete()
                response_data = {
                    'status': 'success',
                    'message': 'Client Details Deleted successfuly.'
                }
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
def getInterventionTypes(request):

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
def saveIntervention(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        intervention_type_code = int(request.POST.get('intervention_type_code'))
        if intervention_type_code is not None and type(intervention_type_code) is int:
            try:
                i_type = InterventionType.objects.get(code__exact=intervention_type_code)
                intervention = Intervention()
                intervention.client = Client.objects.get(id__exact=int(request.POST.get('client')))
                intervention.intervention_type = i_type
                intervention.intervention_date = request.POST.get('intervention_date')
                intervention.created_by = User.objects.get(id__exact=int(request.POST.get('created_by')))
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

                intervention.save()
                # using defer() miraculously solved serialization problem of datetime properties.
                intervention = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created').get(id__exact=intervention.id)

                response_data = {
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
def getInterventionList(request):
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
            list_of_interventions = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created').filter(client__exact=client_id).filter(intervention_type__in=iv_type_ids)

            response_data = {'iv_types': serializers.serialize('json', list_of_related_iv_types),
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
def getIntervention(request):
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
def updateIntervention(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        intervention_id = int(request.POST.get('intervention_id'))
        if intervention_id is not None and type(intervention_id) is int:
            try:
                intervention = Intervention.objects.get(id__exact=intervention_id)
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

                intervention.save()
                # using defer() miraculously solved serialization problem of datetime properties.
                intervention = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created').get(id__exact=intervention.id)
                # construct response

                response_data = {
                    'intervention': serializers.serialize('json', [intervention, ], ensure_ascii=False),
                    'i_type': serializers.serialize('json', [i_type])
                }
                # response_data['intervention'] = serializers.serialize('json', [intervention, ], ensure_ascii=False)
                # response_data['i_type'] = serializers.serialize('json', [i_type])

                return JsonResponse(response_data)
            except Exception as e:
                tb = traceback.format_exc()
                return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception
        else:
            return HttpResponseServerError('Invalid Intervention Type')
    else:
        return PermissionDenied('Operation not allowed. [Missing Permission]')


def deleteIntervention(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        intervention_id = int(request.POST.get('intervention_delete_id'))
        if intervention_id is not None and type(intervention_id) is int:
            try:
                Intervention.objects.filter(pk=intervention_id).delete();
                return JsonResponse(json.dumps({'result': 'success', 'intervention_id': intervention_id}), safe=False)
            except Exception as e:
                tb = traceback.format_exc()
                return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception
        else:
            return HttpResponseServerError('Invalid Intervention Type')
    else:
        return PermissionDenied('Operation not allowed. [Missing Permission]')


def log_me_out(request):
    logout(request)
    return redirect('index')


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
        tb = traceback.format_exc()
        return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception

