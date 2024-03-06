from django.db import models
from foods.models import Food
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderTime = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.orderTime}"

class Quantity(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{order.__str__()} - {self.food.name}"