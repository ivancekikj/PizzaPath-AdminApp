from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.menu.models import Food, Category, Rating, FoodPortion
from apps.menu.serializers import CategorySerializer, FoodSerializer, RatingSerializer, ToppingSerializer, \
    FoodPortionSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(food__foodportion__isnull=False).distinct()
    serializer_class = CategorySerializer
    http_method_names = ["get",]


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    http_method_names = ["get",]

    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id', None)
        category_id = int(category_id) if category_id else None
        foods = Food.objects.filter(foodportion__isnull=False).distinct() if category_id is None else Food.objects.filter(category_id=category_id, foodportion__isnull=False).distinct()
        serialized_data = FoodSerializer(foods, many=True, context={'request': request}).data
        return Response(serialized_data, status=200)


class FoodPortionView(APIView):
    def get(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id', None)
        category_id = int(category_id) if category_id else None
        food_portions = FoodPortion.objects.all() if category_id is None else FoodPortion.objects.filter(food__category_id=category_id)
        serialized_data = FoodPortionSerializer(food_portions, many=True).data
        return Response(serialized_data, status=200)


class RatingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        food_id = request.query_params.get('food_id', None)
        category_id = request.query_params.get('category_id', None)
        if food_id and category_id:
            return Response("category_id and food_id can't be used together.", status=400)
        if food_id is None and category_id is None:
            return Response("category_id or food_id expected.", status=400)
        ratings = Rating.objects.filter(food_id=food_id, user_id=user_id) if food_id else Rating.objects.filter(food__category_id=category_id, user_id=user_id)
        serialized_data = RatingSerializer(data=ratings, many=True).data
        return Response(serialized_data, status=200)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        value = request.data['value']
        food_id = request.data['food_id']
        rating = Rating.objects.create(user_id=user_id, value=value, food_id=food_id)
        rating.save()
        serialized_data = RatingSerializer(data=rating).data
        return Response(serialized_data, status=200)

    def update(self, request, *args, **kwargs):
        user_id = request.user.id
        food_id = request.query_params.get('food_id', None)
        value = request.data['value']

    def delete(self, request, *args, **kwargs):
        return None
