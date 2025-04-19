from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from apps.accounts.views import CustomerView, LogoutView, LoginView
from apps.menu.views import CategoryViewSet, FoodViewSet, FoodPortionView
from apps.orders.views import OrderItemView, CurrentOrderView

router = DefaultRouter()
router.register(r"menu/categories", CategoryViewSet)
router.register(r"menu/foods", FoodViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/menu/food-portions/', FoodPortionView.as_view()),
    path('api/orders/current-order/items/', OrderItemView.as_view()),
    path('api/orders/current-order/', CurrentOrderView.as_view()),
    path('api/accounts/customers/', CustomerView.as_view()),
    path('api/accounts/login/', LoginView.as_view()),
    path('api/accounts/logout/', LogoutView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
