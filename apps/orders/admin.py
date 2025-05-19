import math

from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General Info", {"fields": ("order_number", "customer", "date_time_edited", "status", "description", "number_of_items", "total_price")}),
        ("Order Items", {"fields": ()}),
    )
    list_display = ("customer", "status", "date_time_edited",)
    search_fields = ("customer", "status", "date_time_edited", "description",)
    list_filter = ("status",)

    def order_number(self, obj):
        return obj.id

    def total_price(self, obj):
        total = 0
        for item in obj.orderitem_set.all():
            item_cost = item.food_portion.price
            for topping in item.toppings.all():
                item_cost += topping.price
            item_cost *= item.quantity
            if item.food_portion.discount > 0:
                item_cost *= (1 - item.food_portion.discount)
            total += math.ceil(item_cost)
        return f"{total} ден"

    def number_of_items(self, obj):
        return len(obj.orderitem_set.all())

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return ['order_number', 'description', 'customer', 'date_time_edited', 'total_price', 'number_of_items']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)