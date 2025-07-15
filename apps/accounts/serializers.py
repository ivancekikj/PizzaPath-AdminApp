from rest_framework import serializers

from apps.accounts.models import Customer, CouponReward
from apps.orders.models import OrderItem


class CouponRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponReward
        fields = ['food_portion_id', 'count']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'password', 'is_subscribed_to_newsletter']

    def create(self, data):
        user = Customer.objects.create_user(**data)
        return user
