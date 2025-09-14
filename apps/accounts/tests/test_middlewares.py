from datetime import datetime, timedelta, timezone

from django.http import JsonResponse
from django.test import RequestFactory, TestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.accounts.middlewares import (
    JWTAuthMiddleware,
    JWTRefreshMiddleware,
    RestrictApiAccessMiddleware,
)


class MiddlewareTests(TestCase):
    factory: RequestFactory
    user_id: int
    access_token: str
    refresh_token: str
    dummy_response: callable

    def setUp(self):
        self.factory = RequestFactory()
        self.user_id = 1
        refresh = RefreshToken.for_user(type("User", (), {"id": self.user_id})())
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)

        # Dummy view to simulate a successful endpoint
        self.dummy_response = lambda request: JsonResponse({"ok": True})

    def test_restrict_api_access_blocks_disallowed_origin(self):
        request = self.factory.get("/api/some-endpoint/", HTTP_ORIGIN="http://disallowed.com")
        middleware = RestrictApiAccessMiddleware(self.dummy_response)
        response = middleware(request)
        self.assertEqual(response.status_code, 403)

    def test_restrict_api_access_allows_allowed_origin(self):
        request = self.factory.get("/api/some-endpoint/", HTTP_ORIGIN="http://allowed.com")
        middleware = RestrictApiAccessMiddleware(self.dummy_response)
        response = middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_jwt_auth_middleware_sets_authorization_header(self):
        request = self.factory.get("/api/some-endpoint/")
        request.COOKIES["jwt"] = self.access_token
        middleware = JWTAuthMiddleware(self.dummy_response)
        response = middleware(request)
        self.assertIn("HTTP_AUTHORIZATION", request.META)
        self.assertEqual(request.META["HTTP_AUTHORIZATION"], f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, 200)

    def test_jwt_refresh_middleware_issues_new_access_token(self):
        token = AccessToken.for_user(type("User", (), {"id": self.user_id})())
        token.set_exp(from_time=datetime.now(timezone.utc) - timedelta(hours=2))
        expired_token = str(token)

        request = self.factory.get("/api/some-endpoint/")
        request.COOKIES["jwt"] = expired_token
        request.COOKIES["refresh_token"] = self.refresh_token

        middleware = JWTRefreshMiddleware(self.dummy_response)
        response = middleware(request)

        # Middleware should attach a new cookie in process_response
        response = middleware.process_response(request, response)
        self.assertIn("jwt", response.cookies)
        self.assertNotEqual(response.cookies["jwt"].value, expired_token)

    def test_jwt_refresh_middleware_blocks_when_refresh_invalid(self):
        request = self.factory.get("/api/some-endpoint/")
        request.COOKIES["jwt"] = "invalid.jwt.token"
        request.COOKIES["refresh_token"] = "invalid.refresh.token"

        middleware = JWTRefreshMiddleware(self.dummy_response)
        response = middleware(request)

        self.assertEqual(response.status_code, 401)
