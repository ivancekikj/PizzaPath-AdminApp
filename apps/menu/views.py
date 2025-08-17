from django.db.models import Avg, Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.menu.models import Food, Category, FoodPortion, Rating
from apps.menu.serializers import CategorySerializer, FoodSerializer, FoodPortionSerializer
from apps.orders.models import OrderItemRecord


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


class FoodAverageRatingView(APIView):
    def get(self, request, food_id=None):
        if food_id:
            average = Rating.objects.filter(food_id=food_id).aggregate(avg_score=Avg('value'))["avg_score"]
            return Response(average, status=200)
        food_average_ratings = Food.objects.annotate(avg_value=Avg('rating__value')).values('id', 'avg_value')
        return Response(food_average_ratings, status=200)


class PopularFoodsView(APIView):
    def get(self, request):
        count = request.query_params.get('count', None)
        try:
            count = max(int(count), 1) if count else 4
        except ValueError:
            count = 4

        food_counts = (OrderItemRecord.objects.values("food_portion__food_id")
                       .annotate(total_count=Sum("quantity"))
                       .order_by("-total_count")[:count])
        food_ids = [item["food_portion__food_id"] for item in food_counts]
        index_by_food_id = {food_id: index for index, food_id in enumerate(food_ids)}
        foods = list(Food.objects.filter(id__in=food_ids))
        foods.sort(key=lambda food: index_by_food_id[food.id])

        serialized_data = FoodSerializer(foods, many=True, context={'request': request}).data
        return Response(serialized_data, status=200)
