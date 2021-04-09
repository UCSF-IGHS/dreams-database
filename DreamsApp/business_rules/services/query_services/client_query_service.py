class ClientQueryService:

    def __init__(self, user):
        self.user = user

    def get_clients(self):
        clients = self.user
        if self.user:
            clients = self.user.implementing_partner.select_related('client')
            return clients

