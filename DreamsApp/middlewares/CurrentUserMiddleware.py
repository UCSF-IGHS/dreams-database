from threading import local

_user = local()


class CurrentUserMiddleware(object):
    def process_request(self, request):
        if request.user is not None and request.user.is_authenticated() and request.user.is_active:
            _user.value = request.user
        else:
            _user.value = None


def get_current_user():
    return _user.value
