from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.menu.models import Food, Category, FoodPortion
from apps.menu.serializers import CategorySerializer, FoodSerializer, FoodPortionSerializer


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
