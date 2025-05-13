from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.accounts.models import Customer
from apps.menu.models import Food, FoodPortion, Topping
from django.contrib.auth.models import User


class AbstractOrder(models.Model):
    description = models.TextField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_time_edited = models.DateTimeField(null=False)

    class Meta:
            abstract = True


class AbstractOrderItem(models.Model):
    quantity = models.IntegerField(null=False, validators=[MinValueValidator(1)])

    class Meta:
        abstract = True


class Order(AbstractOrder):
    STATUS_CHOICES = [
        ("edit", "Being edited."),
        ("submitted", "Submitted and awaiting processing."),
        ("preparation", "Currently being prepared."),
        ("delivery", "Currently being delivered."),
    ]

    status = models.CharField(max_length=100, null=False, blank=False, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return f"{self.customer.username} - {self.status}"


class OrderItem(AbstractOrderItem):
    are_coupons_used = models.BooleanField(default=False, null=False)
    date_time_created = models.DateTimeField(default=timezone.now, null=False)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    food_portion = models.ForeignKey(FoodPortion, on_delete=models.SET_NULL, null=True)
    toppings = models.ManyToManyField(Topping)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.order.__str__()} - {self.food_portion.food.name}"
