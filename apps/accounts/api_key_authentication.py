from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        if api_key is None:
            raise AuthenticationFailed('API key missing')
        if api_key != settings.API_KEY:
            raise AuthenticationFailed('Invalid API key')
        return None