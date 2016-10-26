# coding=utf-8
from datetime import datetime, timedelta as t_delta
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from django.conf import  settings

class SessionExpiredMiddleware:
    def process_request(self, request):
        if not request.user.is_authenticated():
            return
        if 'last_activity' not in request.session:
            request.session['last_activity'] = datetime.now()
            return
        last_activity = request.session['last_activity']
        if ((datetime.now() - last_activity).total_seconds()/60) > settings.SESSION_EXPIRY_AGE:
            logout(request)
            if not request.is_ajax():
                return redirect('login')
            else:
                pass # this is an ajax request with a need to login
                response_data = {
                    'status': 'fail',
                    'message': "Your session has expired. You need to login to continue",
                    'ip_users': ''
                }
                return JsonResponse(response_data)
        # If user is within session, set a new last_activity value
        request.session['last_activity'] = datetime.now()
        return