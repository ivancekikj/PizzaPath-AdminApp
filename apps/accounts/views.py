from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from apps.accounts.models import Customer, CouponReward, NewsletterPost
from apps.accounts.serializers import CustomerSerializer, CouponRewardSerializer, NewsletterPostSerializer
from apps.menu.models import FoodRecord
from apps.orders.models import OrderItemRecord


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

    def put(self, request):
        data = {
            "username": request.data.get("username"),
            "address": request.data.get("address"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "phone_number": request.data.get("phone_number"),
            "is_subscribed_to_newsletter": request.data.get("is_subscribed_to_newsletter"),
        }
        for key, value in data.items():
            if value is None:
                return Response(f"{key} expected.", status=400)

        user_id = request.user.id
        customer = Customer.objects.get(id=user_id)
        serializer = CustomerSerializer(instance=customer, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
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
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response

class CustomerOrderedFoodsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        food_ids = FoodRecord.objects.filter(
            foodportionrecord__orderitemrecord__isnull=False
        ).values_list('id', flat=True).distinct()
        return Response(list(food_ids), status=200)


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
        group_by_category = request.query_params.get('group_by_category', None)
        group_by_category = bool(group_by_category) if group_by_category else False

        coupons = list(CouponReward.objects.filter(customer_id=user_id))
        if group_by_category:
            coupons_by_category = {}
            for coupon in coupons:
                category_id = coupon.food_portion.food.category_id
                if category_id not in coupons_by_category:
                    coupons_by_category[category_id] = {
                        "name": coupon.food_portion.food.category.name,
                        "coupons": []
                    }
                coupons_by_category[category_id]["coupons"].append({
                    "food_portion_id": coupon.food_portion_id,
                    "food_name": coupon.food_portion.food.name,
                    "size_name": coupon.food_portion.size.name,
                    "earned_count": coupon.count,
                    "required_amount_for_one_portion": coupon.food_portion.coupon_value,
                })
            return Response(coupons_by_category, status=200)

        serializer = CouponRewardSerializer(coupons, many=True)
        return Response(serializer.data)


class NewsletterPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        page = request.query_params.get('page', None)

        if page is None:
            return Response("page expected.", status=400)
        page = int(page)
        page = max(page, 1)

        posts = Customer.objects.get(id=user_id).received_posts.all().order_by('-date')
        paginator = Paginator(posts, 4)

        try:
            paginated_posts = paginator.page(page)
        except EmptyPage:
            paginated_posts = []

        serialized_posts = NewsletterPostSerializer(paginated_posts, many=True).data
        return Response(serialized_posts, status=200)


class NewsletterPostsCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        number = Customer.objects.get(id=user_id).received_posts.all().count()
        return Response(number, status=200)

