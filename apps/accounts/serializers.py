from rest_framework import serializers

from apps.accounts.models import Customer, CouponReward
from apps.orders.models import OrderItem


class CouponRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponReward
        fields = ['food_portion_id', 'count']


class CustomerSerializer(serializers.ModelSerializer):
    coupons = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'password', 'is_subscribed_to_newsletter', 'coupons']

    def get_coupons(self, obj):
        coupons = CouponReward.objects.filter(customer_id=obj.id)
        order_items = OrderItem.objects.filter(order__customer_id=obj.id,are_coupons_used=True)
        for item in order_items:
            coupons.get(food_portion_id=item.food_portion_id).count -= item.quantity * item.food_portion.coupon_value
        return CouponRewardSerializer(coupons, many=True).data

    def create(self, data):
        user = Customer.objects.create_user(**data)
        return user
