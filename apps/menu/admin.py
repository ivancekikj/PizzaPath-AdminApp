from django.contrib import admin
from django.db.models import Avg

from .models import Food, Category, Topping, FoodPortion, Size, Rating, FoodRecord, FoodPortionRecord, ToppingRecord, \
    CategoryRecord, SizeRecord


class FoodAdmin(admin.ModelAdmin):
    fields = ("name", "category", "description", "image", "toppings", "average_rating")
    list_display = ("name", "category")
    list_filter = ["category"]
    search_fields = ("name", "description")
    readonly_fields = ["average_rating"]
    ordering = ["category", "name"]

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            food_record = FoodRecord(
                id=obj.id,
                name=obj.name,
                description=obj.description,
                image=obj.image,
                category_id=obj.category.id,
            )
            food_record.save()
        else:
            food_record = FoodRecord.objects.get(id=obj.id)
            food_record.name = obj.name
            food_record.description = obj.description
            food_record.image = obj.image
            food_record.category_id = obj.category.id
            food_record.save()

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
    ordering = ["food__category", "food__name", "size"]

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            food_portion_record = FoodPortionRecord(
                id=obj.id,
                size_id=obj.size.id,
                food_id=obj.food.id,
            )
            food_portion_record.save()
        else:
            food_portion_record = FoodPortionRecord.objects.get(id=obj.id)
            food_portion_record.size_id = obj.size.id
            food_portion_record.food_id = obj.food.id
            food_portion_record.save()


class ToppingsAdmin(admin.ModelAdmin):
    search_fields = ["name", "price"]
    ordering = ["name"]

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            topping_record = ToppingRecord(
                id=obj.id,
                name=obj.name,
            )
            topping_record.save()
        else:
            topping_record = ToppingRecord.objects.get(id=obj.id)
            topping_record.name = obj.name
            topping_record.save()


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            category_record = CategoryRecord(
                id=obj.id,
                name=obj.name,
            )
            category_record.save()
        else:
            category_record = CategoryRecord.objects.get(id=obj.id)
            category_record.name = obj.name
            category_record.save()


class SizeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            size_record = SizeRecord(
                id=obj.id,
                name=obj.name,
            )
            size_record.save()
        else:
            size_record = SizeRecord.objects.get(id=obj.id)
            size_record.name = obj.name
            size_record.save()


admin.site.register(Food, FoodAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Topping, ToppingsAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(FoodPortion, FoodPortionAdmin)