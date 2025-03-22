from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from apps.accounts.models import Customer
from apps.accounts.serializers import CustomerSerializer


class CustomerView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(id=user_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(serializer.errors, status=400)


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

        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(status=200)
        response.delete_cookie("jwt")  # Remove the JWT cookie
        return response