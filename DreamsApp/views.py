from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
import traceback
from django.core.exceptions import *
from django.core.urlresolvers import reverse
from django.core import serializers
from django.contrib.auth.models import User
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
                    return HttpResponseRedirect('/clients')

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
                client_list = Woman.objects.all()   # filter to get patients only. Not yet done
                context = {'user': request.user, 'clients': client_list}
                return render(request, 'clients.html', context)
            elif request.method == 'POST' and request.is_ajax():
                search_value = request.POST.get('searchValue', '')
                search_result = Woman.objects.filter(Q(first_name__startswith=search_value) |
                                                    Q(last_name__startswith=search_value) |
                                                    Q(middle_name__startswith=search_value))
                return JsonResponse(serializers.serialize('json', search_result), safe=False)
        else:
            return render(request, 'index.html')
    except:
        return render(request, 'index.html')


def client_profile(request):
    if request.user is not None and request.user.is_authenticated() and request.user.is_active:
        if request.method == 'GET':
            client_id = int(request.GET['client_id'])
        else:
            client_id = int(request.POST('client_id', ''))

        if client_id is not None and client_id != 0:
            try:
                client_found = Woman.objects.get(id=client_id)
                if client_found is not None:
                    return render(request, 'client_profile.html', {'client': client_found, 'user': request.user})
            except:
                return render(request, 'index.html')
    return render(request, 'index.html')


def testajax(request):
    return render(request, 'testAjax.html')

# Use /ivgetTypes/ in the post url to access the method
def getInterventionTypes(request):
    # Handles post request for intervention types.
    # Receives category_code from request and searches for types in the database
    if request.method == 'POST':
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

    # Determine if request is for save or edit

    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        intervention_type_code = int(request.POST.get('intervention_type_code'))
        if intervention_type_code is not None and type(intervention_type_code) is int:
            try:
                i_type = InterventionType.objects.get(code__exact=intervention_type_code)
                intervention = Intervention()
                intervention.client = Woman.objects.get(id__exact=int(request.POST.get('client')))
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
                intervention = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created').get(id__exact=intervention.id)
                # There is trouble handling dates. This needs to be fixed asap
                # intervention.date_changed = None
                # intervention.intervention_date = None
                # intervention.date_created = None
                # construct response

                response_data = {}
                response_data['intervention'] = serializers.serialize('json', [intervention, ], ensure_ascii=False)
                response_data['i_type'] = serializers.serialize('json', [i_type])

                return JsonResponse(response_data)
            except Exception as e:
                tb = traceback.format_exc()
                return HttpResponseServerError(tb)  # for debugging purposes. Will only report exception
        else:
            return HttpResponseServerError('Invalid Intervention Type')
    else:
        return PermissionDenied('Operation not allowed. [Missing Permissions]')

# method that returns a list of interventions of given category for a given client
# use /ivList/ url pattern to access the method
def getInterventionList(request):
    if request.method == 'POST' and request.user is not None and request.user.is_authenticated():
        client_id = request.POST.get('client_id')
        intervention_category_code = request.POST.get('intervention_category_code')

        iv_category = InterventionCategory.objects.get(code__exact=intervention_category_code)
        list_of_related_iv_types = InterventionType.objects.filter(intervention_category__exact=iv_category)
        iv_type_ids = [i_type.id for i_type in list_of_related_iv_types]
        list_of_interventions = Intervention.objects.defer('date_changed', 'intervention_date', 'date_created').filter(client__exact=client_id).filter(intervention_type__in=iv_type_ids)

        response_data = {'iv_types': serializers.serialize('json', list_of_related_iv_types),
                         'interventions': serializers.serialize('json', list_of_interventions)
                         }
        return JsonResponse(response_data)
    else:
        return PermissionDenied('Missing permissions')

# method for viewing and editing and intervention
def viewIntervention(request):
    if request.method == 'GET' and request.user is not None and request.user.is_authenticated():
        if 'intervention_id' not in request.GET.keys():
            return HttpResponseServerError('Invalid Request')



