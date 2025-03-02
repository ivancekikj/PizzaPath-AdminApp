from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.accounts.models import Customer
from apps.menu.models import Food, FoodPortion, Topping
from django.contrib.auth.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ("edit", "Being edited."),
        ("submitted", "Submitted and awaiting processing."),
        ("preparation", "Currently being prepared."),
        ("delivery", "Currently being delivered."),
        ("closed", "Delivered and paid."),
    ]

    date_time_edited = models.DateTimeField(null=False)
    status = models.CharField(max_length=100, null=False, blank=False, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    description = models.TextField(null=True)

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.customer.username} - {self.status}"


class OrderItem(models.Model):
    quantity = models.IntegerField(null=False, validators=[MinValueValidator(1)])
    discount = models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    price = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
    are_coupons_used = models.BooleanField(default=False, null=False)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    food_portion = models.ForeignKey(FoodPortion, on_delete=models.SET_NULL, null=True)
    toppings = models.ManyToManyField(Topping)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.order.__str__()} - {self.food_portion.food.name}"
