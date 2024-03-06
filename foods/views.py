from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Food

def food(request, foodName):
    if request.method == "GET":
        try:
            food = Food.objects.get(name=foodName)
            response = json.dumps([{"food": food.name, "price": food.priceMKD}])
        except:
            response = json.dumps([{"error": "No food found"}])
    return HttpResponse(response, content_type="text/json")