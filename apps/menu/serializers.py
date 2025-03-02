from django.db.models import Avg
from rest_framework import serializers
from .models import Category, Food, Rating, Topping


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Food
        exclude = ("image",)

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

    def get_average_rating(self, obj):
        return Rating.objects.filter(food_id=obj.id).aggregate(avg_score=Avg('value'))["avg_score"]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("user",)
