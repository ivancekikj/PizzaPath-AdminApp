from rest_framework import viewsets
from rest_framework.response import Response

from apps.menu.models import Food, Category
from apps.menu.serializers import CategorySerializer, FoodSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    http_method_names = ["get",]


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    http_method_names = ["get",]

    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id', None)
        if category_id is None:
            return Response("category_id is required", status=400)
        foods = Food.objects.filter(category_id=category_id)
        serialized_data = FoodSerializer(foods, many=True).data
        return Response(serialized_data, status=200)