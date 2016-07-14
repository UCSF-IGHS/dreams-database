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
from django.conf.urls import url
from django.contrib import admin
from DreamsApp import views

urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    url(r'^clients/$', views.clients, name='clients'),
    url(r'^clientSave/$', views.save_client, name='save_client'),
    url(r'^clientEdit/$', views.edit_client, name='edit_client'),
    url(r'^clientDelete/$', views.delete_client, name='delete_client'),
    url(r'^client/$', views.client_profile),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^ivgetTypes/$', views.get_intervention_types),
    url(r'^ivSave/$', views.save_intervention),
    url(r'^ivList/$', views.get_intervention_list),
    url(r'^ivGet/$', views.get_intervention),
    url(r'^ivUpdate/$', views.update_intervention),
    url(r'^ivDelete/$', views.delete_intervention),
    url(r'^intervention/$', views.testajax),
    url(r'^getSubCounties/$', views.get_sub_counties),
    url(r'^getWards/$', views.get_wards),
    url(r'^logout/$', views.log_me_out),
    url(r'^reporting/$', views.reporting, name='reporting'),
    url(r'^help/$', views.user_help, name='user_help'),
    url(r'^logs/$', views.logs, name='logs'),
]
