from django.shortcuts import render, redirect
from apps.menu.models import Category, Food


def order(request):
    if request.method == "POST":
        return render(request, "pages/index.html")
    else:
        foods = {}
        categories = []
        for category in Category.objects.all():
            foods[category.name.capitalize()] = Food.objects.filter(category=category)
            categories.append(category.name.capitalize())
        context = {
            "foods": foods,
            "categories": categories
        }
        return render(request, "orders/order.html", context)