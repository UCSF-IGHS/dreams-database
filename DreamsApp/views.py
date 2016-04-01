from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from DreamsApp.models import *

def index(request):
    if request.method == 'GET':
        context = {'message':'Please login to continue'}
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
                    patients = User.objects.all(); # filter to get patients only. Not yet done
                    context = {'woman': user, 'patients': patients}
                    return render(request, 'dashboard.html', context)
                else:
                    return HttpResponse("Login Successful, but the account has been disabled!")
            else:
                return HttpResponse('Login Failed')
    else:
        return render(request, 'index.html')


def dashboard(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            context = {'user':request.user}
            return render(request, 'dashboard.html', context)
        else:
            return render(request, 'index.html')
    except:
        return render(request, 'index.html')


def patient(request):
    try:
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            return render(request, 'patient.html')
        else:
            return render(request, 'index.html')
    except:
        return render(request, 'index.html')

