from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from apps.accounts.views import CustomerView, LogoutView, LoginView, CouponRewardView, CurrentCustomerView, \
    NewsletterPostsView, NewsletterPostsCountView, CustomerOrderedFoodsView, RatingView
from apps.menu.views import CategoryViewSet, FoodViewSet, FoodPortionView, FoodAverageRatingView, PopularFoodsView
from apps.orders.views import OrderItemView, CurrentOrderView, OrderCouponRewardView

router = DefaultRouter()
router.register(r"menu/categories", CategoryViewSet)
router.register(r"menu/foods", FoodViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/menu/food-portions/', FoodPortionView.as_view()),
    path('api/menu/foods/average-ratings/', FoodAverageRatingView.as_view()),
    path('api/menu/foods/<int:food_id>/average-rating/', FoodAverageRatingView.as_view()),
    path('api/menu/most-popular-foods/', PopularFoodsView.as_view()),
    path('api/orders/current-order/items/', OrderItemView.as_view()),
    path('api/orders/current-order/items/<int:id>/', OrderItemView.as_view()),
    path('api/orders/current-order/', CurrentOrderView.as_view()),
    path('api/orders/current-order/coupon-info', OrderCouponRewardView.as_view()),
    path('api/accounts/customers/', CustomerView.as_view()),
    path('api/accounts/customers/logged-in-customer/', CurrentCustomerView.as_view()),
    path('api/accounts/customers/logged-in-customer/ordered-foods/ids/', CustomerOrderedFoodsView.as_view()),
    path('api/accounts/customers/logged-in-customer/coupons/', CouponRewardView.as_view()),
    path('api/accounts/customers/logged-in-customer/food-ratings/', RatingView.as_view()),
    path('api/accounts/login/', LoginView.as_view()),
    path('api/accounts/logout/', LogoutView.as_view()),
    path('api/accounts/customers/received-posts/', NewsletterPostsView.as_view()),
    path('api/accounts/customers/received-posts/count/', NewsletterPostsCountView.as_view()),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
