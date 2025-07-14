from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import CouponReward
from apps.accounts.serializers import CouponRewardSerializer
from apps.menu.models import FoodPortion, Topping
from apps.orders.models import Order, OrderItem
from apps.orders.serialiers import OrderSerializer


class OrderItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        quantity = request.data.get('quantity', None)
        food_portion_id = request.data.get('food_portion_id', None)
        are_coupons_used = request.data.get('are_coupons_used', False)
        toppings_ids = request.data.get('toppings_ids', [])
        user_id = request.user.id

        if quantity is None:
            return Response("quantity expected.", status=400)
        if food_portion_id is None:
            return Response("food_portion_id expected.", status=400)

        order = get_current_order(user_id)
        food_portion = FoodPortion.objects.get(id=food_portion_id)
        toppings = Topping.objects.filter(id__in=toppings_ids) if toppings_ids and len(toppings_ids) > 0 else []

        if order is None:
            order = Order.objects.create(customer_id=user_id, date_time_edited=datetime.now())
            order.save()
        elif not check_if_editable(order):
            return Response("order is not editable.", status=400)

        order_item = OrderItem.objects.create(
            quantity=quantity,
            order=order,
            food_portion=food_portion,
            are_coupons_used=are_coupons_used,
        )
        order_item.save()
        order_item.toppings.add(*toppings)
        order_item.save()

        return Response(status=200)

    def put(self, request, *args, **kwargs):
        item_id = kwargs.get('id')
        quantity = request.data.get('quantity', None)
        food_portion_id = request.data.get('food_portion_id', None)
        toppings_ids = request.data.get('toppings_ids', [])
        user_id = request.user.id

        if quantity is None:
            return Response("quantity expected.", status=400)
        if food_portion_id is None:
            return Response("food_portion_id expected.", status=400)

        order = get_current_order(user_id)
        if not check_if_editable(order):
            return Response("order is not editable.", status=400)

        order_item = OrderItem.objects.get(id=item_id, order__customer_id=user_id)
        if order_item is None:
            return Response("order_item not found.", status=404)

        order_item.quantity = quantity
        order_item.food_portion = FoodPortion.objects.get(id=food_portion_id)
        order_item.toppings.clear()
        toppings = Topping.objects.filter(id__in=toppings_ids) if toppings_ids and len(toppings_ids) > 0 else []
        order_item.toppings.add(*toppings)
        order_item.save()

        update_order_date(order)
        order.save()

        return Response(status=200)

    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get('id')
        user_id = request.user.id

        order = get_current_order(user_id)
        if not check_if_editable(order):
            return Response("order is not editable.", status=400)

        order_item = OrderItem.objects.get(id=item_id, order__customer_id=user_id)
        if order_item is None:
            return Response("order_item not found.", status=404)

        order_item.delete()
        update_order_date(order)
        order.save()

        return Response(status=200)


class CurrentOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        order = get_current_order(user_id)
        if order is None:
            return Response(None, status=200)
        serialized_data = OrderSerializer(order, context={'request': request}).data
        return Response(serialized_data, status=200)

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        description = request.data.get('description', None)
        submitted = request.data.get('submitted', None)

        order = get_current_order(user_id)
        if order is None:
            return Response("order not found.", status=404)
        if not check_if_editable(order):
            return Response("order is not editable.", status=400)

        if description:
            order.description = description
            update_order_date(order)
        elif submitted is not None and submitted is True:
            order.status = Order.STATUS_CHOICES[1][0]
            update_order_date(order)
        order.save()

        return Response(status=200)

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        order = get_current_order(user_id)

        if order is None:
            return Response("order not found.", status=404)
        if not check_if_editable(order):
            return Response("order is not editable.", status=400)

        order.delete()

        return Response(status=200)


class OrderCouponRewardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        order = get_current_order(user_id)
        if order is None:
            return Response(None, status=200)
        earned_coupons, redeemed_coupons = 0, 0
        coupon_by_portion = {coupon.food_portion_id: coupon for coupon in CouponReward.objects.filter(customer_id=user_id)}
        order_items = OrderItem.objects.filter(order__customer_id=user_id,are_coupons_used=True)
        for item in order_items:
            redeemed_coupons += item.quantity * item.food_portion.coupon_value
            earned_coupons += item.quantity
            coupon_by_portion[item.food_portion_id].count -= item.quantity * item.food_portion.coupon_value
        return Response({
            "coupons": CouponRewardSerializer(list(coupon_by_portion.values()), many=True).data,
            "earned_coupons": earned_coupons,
            "redeemed_coupons": redeemed_coupons,
        }, status=200)


def check_if_editable(order: Order):
    if order.status == Order.STATUS_CHOICES[0][0]:
        return True
    return False


def update_order_date(order: Order):
    order.date_time_edited = datetime.now()


def get_current_order(user_id):
    return Order.objects.filter(customer_id=user_id).first()
