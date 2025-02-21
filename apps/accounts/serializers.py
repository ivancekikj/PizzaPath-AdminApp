from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from apps.accounts.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'password', 'is_subscribed_to_newsletter']

    def create(self, data):
        user = Customer.objects.create_user(**data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.is_staff:
            raise serializers.ValidationError("Only customers are allowed to log in.")
        return data
