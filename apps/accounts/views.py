from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from apps.accounts.models import Customer, CouponReward
from apps.accounts.serializers import CustomerSerializer, CouponRewardSerializer


class CustomerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(serializer.errors, status=400)


class CurrentCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(id=user_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None or user.is_staff:
            return Response({"detail": "No account with the given credentials found."}, status=400)

        refresh = RefreshToken.for_user(user)
        response = Response(status=200)

        response.set_cookie(
            key="jwt",
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(status=200)
        response.delete_cookie("jwt")
        response.delete_cookie("refresh_token")
        return response


class CouponRewardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        coupons = CouponReward.objects.filter(customer_id=user_id)
        serializer = CouponRewardSerializer(coupons, many=True)
        return Response(serializer.data)