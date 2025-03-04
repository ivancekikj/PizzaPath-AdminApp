from django.conf import settings
from django.http import HttpResponseForbidden

class RestrictApiAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG:
            if request.path.startswith('/api/'):
                origin = request.META.get('HTTP_ORIGIN')
                allowed_origins = settings.CORS_ALLOWED_ORIGINS
                if origin and origin not in allowed_origins:
                    return HttpResponseForbidden("Access denied")
        response = self.get_response(request)
        return response