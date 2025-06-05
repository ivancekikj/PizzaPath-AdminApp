import math

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Order, OrderRecord, OrderItemRecord, OrderItemToppingRecord


class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General Info", {"fields": ("order_number", "customer", "date_time_edited", "status", "description", "number_of_items", "total_price")}),
        ("Order Items", {"fields": ("items",)}),
    )
    list_display = ("customer", "status", "date_time_edited",)
    search_fields = ("customer", "status", "date_time_edited", "description",)
    list_filter = ("status",)

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(status=Order.STATUS_CHOICES[0][0])

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

    def items(self, obj):
        result = ""
        for i, item in enumerate(obj.orderitem_set.all().order_by("-date_time_created"), start=1):
            digits_space = '&nbsp;' * (len(str(i)) + 3)
            item_price = item.food_portion.price
            result += f"{i}. Food name: {item.food_portion.food.name}</br>"
            result += f"{digits_space}Food portion: {item.food_portion.size.name} ({item.food_portion.price} ден)</br>"
            result += f"{digits_space}Quantity: {item.quantity}</br>"
            if item.food_portion.discount > 0:
                result += f"{digits_space}Discount: {int(item.food_portion.discount * 100)}%</br>"
            if item.toppings and len(item.toppings.all()) > 0:
                result += f"{digits_space}Toppings:</br>"
                for j, topping in enumerate(item.toppings.all(), start=1):
                    result += f"{digits_space}{'&nbsp;' * 4}{j}. {topping.name} ({topping.price} ден)</br>"
                    item_price += topping.price
            item_price *= item.quantity
            item_price *= (1 - item.food_portion.discount) if item.food_portion.discount > 0 else 1
            item_price = math.ceil(item_price)
            result += f"{digits_space}Item price: {item_price} ден</br></br>"
        return format_html(result)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.date_time_edited = timezone.now()
        obj.save()
        if obj.status == Order.STATUS_CHOICES[4][0]:
            order_record = OrderRecord(
                id=obj.id,
                customer=obj.customer,
                date_time_edited=obj.date_time_edited,
                description=obj.description
            )
            order_record.save()
            for item in obj.orderitem_set.all():
                item_record = OrderItemRecord(
                    id=item.id,
                    order=order_record,
                    food_portion_id=item.food_portion.id,
                    quantity=item.quantity,
                    discount=item.food_portion.discount,
                    price=item.food_portion.price,
                    coupons_used=0
                )
                item_record.save()
                for topping in item.toppings.all():
                    item_topping_record = OrderItemToppingRecord(
                        topping_id=topping.id,
                        order_item=item_record,
                        price=topping.price
                    )
                    item_topping_record.save()
            obj.delete()

    def get_readonly_fields(self, request, obj=None):
        return ['order_number', 'description', 'customer', 'date_time_edited', 'total_price', 'number_of_items', 'items']


class OrderRecordAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General Info", {"fields": ("order_number", "customer", "date_time_edited", "description", "number_of_items")}),
        #("Order Items", {"fields": ("items",)}),
    )
    list_display = ("customer", "date_time_edited",)
    search_fields = ("customer", "date_time_edited", "description",)
    ordering = ("-date_time_edited",)

    def number_of_items(self, obj):
        return len(obj.orderitemrecord_set.all())

    def order_number(self, obj):
        return obj.id

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderRecord, OrderRecordAdmin)