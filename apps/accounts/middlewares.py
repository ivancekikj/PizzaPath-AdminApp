from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = request.COOKIES.get("jwt")
        if jwt_token:
            request.META["HTTP_AUTHORIZATION"] = (
                f"Bearer {request.new_access_token if getattr(request, 'refresh_token_used', False) else jwt_token}"
            )
        return self.get_response(request)


class JWTRefreshMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("jwt")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return None

        try:
            AccessToken(access_token)
        except TokenError:
            if not refresh_token:
                return JsonResponse({"error": "Session expired, please log in again."}, status=401)

            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)

                request.new_access_token = new_access_token

                request.refresh_token_used = True
            except TokenError:
                return JsonResponse({"error": "Refresh token expired, please log in again."}, status=401)

        return None

    def process_response(self, request, response):
        if getattr(request, "refresh_token_used", False):
            response.set_cookie(
                key="jwt",
                value=request.new_access_token,
                httponly=True,
                secure=True,
                samesite="Lax",
            )
        return response
