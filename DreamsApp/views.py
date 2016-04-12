from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json # this is for non-query sets
from django.core import serializers  # this is for query set
from django.http import HttpResponseRedirect
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


