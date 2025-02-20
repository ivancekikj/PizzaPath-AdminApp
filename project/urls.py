from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from apps.menu.views import CategoryViewSet, FoodViewSet

router = DefaultRouter()
router.register(r"menu/categories", CategoryViewSet)
router.register(r"menu/foods", FoodViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
