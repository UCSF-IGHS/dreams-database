from threading import local

_user = local()


class CurrentUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        if request.user is not None and request.user.is_authenticated and request.user.is_active:
            _user.value = request.user
        else:
            _user.value = None


def get_current_user():
    #return _user.value if hasattr(_user, 'value') else None
    return getattr(_user, "value", None)
