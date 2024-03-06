from django.urls import path
from .views import food

urlpatterns = [
    path("<str:foodName>", food, name="food")
]