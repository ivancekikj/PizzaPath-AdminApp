from rest_framework import serializers

from apps.accounts.models import Customer, CouponReward, NewsletterPost
from apps.menu.models import Rating


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


class NewsletterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterPost
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("food_id", "value",)