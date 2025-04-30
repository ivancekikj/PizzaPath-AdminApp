from rest_framework import serializers

from apps.menu.models import FoodPortion
from apps.menu.serializers import FoodPortionSerializer, FoodSerializer
from apps.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    food_portion_id = serializers.SerializerMethodField()
    topping_ids = serializers.SerializerMethodField()
    food = serializers.SerializerMethodField()
    food_portions = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("id", "food", "food_portions", "quantity", "food_portion_id", "topping_ids", "are_coupons_used",)

    def get_food_portion_id(self, obj):
        return obj.food_portion.id

    def get_topping_ids(self, obj):
        return [topping.id for topping in obj.toppings.all()]

    def get_food(self, obj):
        return FoodSerializer(obj.food_portion.food, context=self.context).data

    def get_food_portions(self, obj):
        food_portions = FoodPortion.objects.filter(food_id=obj.food_portion.food.id)
        return FoodPortionSerializer(food_portions, many=True).data


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "date_time_edited", "status", "description", "items")

    def get_items(self, obj):
        items = OrderItem.objects.filter(order_id=obj.id).order_by("-date_time_created")
        return OrderItemSerializer(items, many=True, context=self.context).data