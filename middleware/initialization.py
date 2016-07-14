from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group

from DreamsApp.models import InitApp

import datetime


class InitializationMiddleware(object):
    def process_request(self, request):
        # check if application is initialized
        if InitApp.objects.all().count() < 1:
            try:
                # create permission
                content_type = ContentType.objects.get_for_model(Group)

                if Permission.objects.filter(codename='can_view_other_ip_data').count() < 1:
                    permission = Permission.objects.create(codename='can_view_other_ip_data',
                                                           name='Can View Other IP Data',
                                                           content_type=content_type)
                if Permission.objects.filter(codename='can_search_client_by_name').count() < 1:
                    permission = Permission.objects.create(codename='can_search_client_by_name',
                                                           name='Can Search Client By Name',
                                                           content_type=content_type)
                if Permission.objects.filter(codename='can_edit_neighbour_intervention').count() < 1:
                    permission = Permission.objects.create(codename='can_edit_neighbour_intervention',
                                                           name='Can Edit Intervention Entered By A Different User',
                                                           content_type=content_type)
                if Permission.objects.filter(codename='can_view_records_older_than_a_week').count() < 1:
                    permission = Permission.objects.create(codename='can_view_records_older_than_a_week',
                                                           name='Can View Records Older Than A Week',
                                                           content_type=content_type)
                if Permission.objects.filter(codename='can_view_logs').count() < 1:
                    permission = Permission.objects.create(codename='can_view_logs',
                                                           name='Can View Logs',
                                                           content_type=content_type)
                init_app = InitApp(
                    timestamp=datetime.datetime.now(),
                    inited=True
                )
                init_app.save()
            except Exception as e:
                return None
        return None