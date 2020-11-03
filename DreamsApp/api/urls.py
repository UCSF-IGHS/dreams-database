from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from DreamsApp.api.views import interventions_view


urlpatterns = [
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(r'^api/v1/interventions-create/$',
        csrf_exempt(interventions_view.InterventionCreateView.as_view()), name='interventions_api'),
    url(r'^api/v1/interventions/$',
        csrf_exempt(interventions_view.InterventionMultipleCreateView.as_view()), name='interventions-multiple_api'),
]
