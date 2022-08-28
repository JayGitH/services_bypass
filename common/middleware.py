from django.utils.deprecation import MiddlewareMixin


class InjectUserInfoMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        setattr(request, '_dont_enforce_csrf_checks', True)
