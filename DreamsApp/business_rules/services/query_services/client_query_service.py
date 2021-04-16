from DreamsApp.models import Client


class ClientQueryService:

    def __init__(self, user):
        self.user = user

    def get_clients(self):
       return Client.objects.none()

