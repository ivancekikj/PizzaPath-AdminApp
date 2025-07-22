import math

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Order, OrderRecord, OrderItemRecord, OrderItemToppingRecord
from ..accounts.models import CouponReward


class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General Info", {"fields": ("order_number", "customer", "date_time_edited", "status", "description", "number_of_items", "number_of_earned_coupons", "number_of_redeemed_coupons", "total_price")}),
        ("Order Items", {"fields": ("items",)}),
    )
    list_display = ("customer", "status", "date_time_edited",)
    search_fields = ("customer", "status", "date_time_edited", "description",)
    list_filter = ("status",)

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(status=Order.STATUS_CHOICES[0][0])

    def order_number(self, obj):
        return obj.id

    def number_of_earned_coupons(self, obj):
        total = 0
        for item in obj.orderitem_set.all():
            if item.are_coupons_used:
                total += item.quantity
        return total

    def number_of_redeemed_coupons(self, obj):
        total = 0
        for item in obj.orderitem_set.all():
            if item.are_coupons_used:
                total += item.quantity * item.food_portion.coupon_value
        return total

    def total_price(self, obj):
        total = 0
        for item in obj.orderitem_set.all():
            item_cost = 0 if item.are_coupons_used else item.food_portion.price
            if not item.are_coupons_used:
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
            item_price = 0 if item.are_coupons_used else item.food_portion.price
            result += f"{i}. Food name: {item.food_portion.food.name}</br>"
            result += f"{digits_space}Food portion: {item.food_portion.size.name} ({item.food_portion.price} ден)</br>"
            result += f"{digits_space}Quantity: {item.quantity}</br>"
            result += f"{digits_space}Number of coupons used: {0 if not item.are_coupons_used else item.quantity * item.food_portion.coupon_value}</br>"
            result += f"{digits_space}Number of coupons earned: {0 if not item.are_coupons_used else item.quantity}</br>"
            if item.food_portion.discount > 0:
                result += f"{digits_space}Discount: {int(item.food_portion.discount * 100)}%</br>"
            if item.toppings and len(item.toppings.all()) > 0:
                result += f"{digits_space}Toppings:</br>"
                for j, topping in enumerate(item.toppings.all(), start=1):
                    result += f"{digits_space}{'&nbsp;' * 4}{j}. {topping.name} ({topping.price} ден)</br>"
                    if not item.are_coupons_used:
                        item_price += topping.price
            if not item.are_coupons_used:
                item_price *= item.quantity
                if item.food_portion.discount > 0:
                    item_price *= (1 - item.food_portion.discount)
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
            # Convert order, items and toppings to records
            order_record = OrderRecord(
                id=obj.id,
                customer=obj.customer,
                date_time_edited=obj.date_time_edited,
                description=obj.description
            )
            order_record.save()
            items_with_coupons = []
            for item in obj.orderitem_set.all():
                item_record = OrderItemRecord(
                    id=item.id,
                    order=order_record,
                    date_time_created=item.date_time_created,
                    food_portion_id=item.food_portion.id,
                    quantity=item.quantity,
                    discount=item.food_portion.discount,
                    price=item.food_portion.price,
                    coupons_used=0 if not item.are_coupons_used else item.quantity * item.food_portion.coupon_value
                )
                item_record.save()
                for topping in item.toppings.all():
                    item_topping_record = OrderItemToppingRecord(
                        topping_id=topping.id,
                        order_item=item_record,
                        price=topping.price
                    )
                    item_topping_record.save()
                if item.are_coupons_used:
                    items_with_coupons.append(item)
            # Update coupon counts
            portion_ids = {item.food_portion_id for item in items_with_coupons}
            coupon_by_portion = {coupon.food_portion_id: coupon for coupon in CouponReward.objects.filter(customer_id=obj.customer_id,food_portion_id__in=portion_ids)}
            for item in items_with_coupons:
                coupon = coupon_by_portion.get(item.food_portion_id)
                coupon.count -= item.quantity * item.food_portion.coupon_value
                coupon.count += item.quantity
            for coupon in coupon_by_portion.values():
                coupon.save()
            # Cascade delete active order
            obj.delete()

    def get_readonly_fields(self, request, obj=None):
        return ['order_number', 'description', 'customer', 'date_time_edited', 'total_price', 'number_of_items', 'items', 'number_of_earned_coupons', 'number_of_redeemed_coupons']


class OrderRecordAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General Info", {"fields": ("order_number", "customer", "date_time_edited", "description", "number_of_items", "number_of_earned_coupons", "number_of_redeemed_coupons", "total_price")}),
        ("Order Items", {"fields": ("items",)}),
    )
    list_display = ("customer", "date_time_edited",)
    search_fields = ("customer__username", "date_time_edited", "description",)
    ordering = ("-date_time_edited",)

    def number_of_earned_coupons(self, obj):
        total = 0
        for item in obj.orderitemrecord_set.all():
            if item.coupons_used > 0:
                total += item.quantity
        return total

    def number_of_redeemed_coupons(self, obj):
        total = 0
        for item in obj.orderitemrecord_set.all():
            total += item.coupons_used
        return total

    def items(self, obj):
        result = ""
        for i, item in enumerate(obj.orderitemrecord_set.all().order_by("-date_time_created"), start=1):
            digits_space = '&nbsp;' * (len(str(i)) + 3)
            item_price = 0 if item.coupons_used > 0 else item.price
            result += f"{i}. Food name: {item.food_portion.food.name}</br>"
            result += f"{digits_space}Food portion: {item.food_portion.size.name} ({item.price} ден)</br>"
            result += f"{digits_space}Quantity: {item.quantity}</br>"
            result += f"{digits_space}Number of coupons used: {item.coupons_used}</br>"
            result += f"{digits_space}Number of coupons earned: {0 if item.coupons_used == 0 else item.quantity}</br>"
            if item.discount > 0:
                result += f"{digits_space}Discount: {int(item.discount * 100)}%</br>"
            if item.orderitemtoppingrecord_set.exists():
                result += f"{digits_space}Toppings:</br>"
                for j, topping in enumerate(item.orderitemtoppingrecord_set.all(), start=1):
                    result += f"{digits_space}{'&nbsp;' * 4}{j}. {topping.topping.name} ({topping.price} ден)</br>"
                    if item.coupons_used == 0:
                        item_price += topping.price
            if item.coupons_used == 0:
                item_price *= item.quantity
                item_price *= (1 - item.discount) if item.discount > 0 else 1
                item_price = math.ceil(item_price)
            result += f"{digits_space}Item price: {item_price} ден</br></br>"
        return format_html(result)

    def total_price(self, obj):
        total = 0
        for item in obj.orderitemrecord_set.all():
            item_cost = 0 if item.coupons_used > 0 else item.price
            if item.coupons_used == 0:
                for topping in item.orderitemtoppingrecord_set.all():
                    item_cost += topping.price
                item_cost *= item.quantity
                if item.discount > 0:
                    item_cost *= (1 - item.discount)
            total += math.ceil(item_cost)
        return f"{total} ден"

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