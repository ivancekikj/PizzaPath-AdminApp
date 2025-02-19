from django.contrib import admin
from .models import Food, Category, Topping, FoodPortion, Size, Rating

admin.site.register(Food)
admin.site.register(Category)
admin.site.register(Topping)
admin.site.register(Size)
admin.site.register(FoodPortion)
admin.site.register(Rating)