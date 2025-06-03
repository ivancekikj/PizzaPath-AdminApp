from django.contrib import admin
from django.db.models import Avg

from .models import Food, Category, Topping, FoodPortion, Size, Rating

class FoodAdmin(admin.ModelAdmin):
    fields = ("name", "category", "description", "image", "toppings", "average_rating")
    list_display = ("name", "category")
    list_filter = ["category"]
    search_fields = ("name", "description")
    readonly_fields = ["average_rating"]

    def average_rating(self, obj):
        ratings = Rating.objects.filter(food_id=obj.id)
        if ratings.exists():
            return f"{ratings.aggregate(Avg('value'))['value__avg']:.2f} / 5"
        return "/"


class FoodPortionAdmin(admin.ModelAdmin):
    fields = ["food", "size", "price", "discount", "coupon_value", "is_available"]
    list_display = ["food", "food__category", "size", "is_available"]
    list_filter = ["size", "is_available", "food__category"]
    search_fields = ["food__name", "price", "discount", "coupon_value"]


class ToppingsAdmin(admin.ModelAdmin):
    search_fields = ["name", "price"]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class SizeAdmin(admin.ModelAdmin):
    search_fields = ["name", "description"]


admin.site.register(Food, FoodAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Topping, ToppingsAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(FoodPortion, FoodPortionAdmin)