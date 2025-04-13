from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.menu.models import FoodPortion, Topping
from apps.orders.models import Order, OrderItem


class OrderItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        quantity = request.data.get('quantity', None)
        food_portion_id = request.data.get('food_portion_id', None)
        toppings_ids = request.data.get('toppings_ids', [])
        user_id = request.user.id

        if quantity is None:
            return Response("quantity expected.", status=400)
        if food_portion_id is None:
            return Response("food_portion_id expected.", status=400)

        order = Order.objects.filter(customer_id=user_id).exclude(status="closed").first()
        food_portion = FoodPortion.objects.get(id=food_portion_id)
        toppings = Topping.objects.filter(id__in=toppings_ids) if toppings_ids and len(toppings_ids) > 0 else []
        if order is None:
            order = Order.objects.create(customer_id=user_id, date_time_edited=datetime.now())
            order.save()
        order_item = OrderItem.objects.create(
            quantity=quantity,
            discount = food_portion.discount,
            price=food_portion.price,
            order=order,
            food_portion=food_portion,
        )
        order_item.save()
        order_item.toppings.add(*toppings)
        order.date_time_edited = datetime.now()
        order_item.save()

        return Response(status=200)