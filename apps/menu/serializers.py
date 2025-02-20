from rest_framework import serializers
from .models import Category, Food


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Food
        exclude = ("image",)

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)