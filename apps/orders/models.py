from operator import index

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.accounts.models import Customer
from apps.menu.models import Food, FoodPortion, Topping, FoodPortionRecord, ToppingRecord
from django.contrib.auth.models import User


class AbstractOrder(models.Model):
    description = models.TextField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_time_edited = models.DateTimeField(null=False)

    class Meta:
            abstract = True


class AbstractOrderItem(models.Model):
    quantity = models.IntegerField(null=False, validators=[MinValueValidator(1)], default=1)
    date_time_created = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        abstract = True


class Order(AbstractOrder):
    STATUS_CHOICES = [
        ("edit", "edit"),
        ("submitted", "submitted"),
        ("preparation", "preparation"),
        ("delivery", "delivery"),
        ("closed", "closed"),
    ]

    status = models.CharField(max_length=100, null=False, blank=False, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    class Meta:
        verbose_name = "Active Order"
        verbose_name_plural = "Active Orders"

    @staticmethod
    def find_index_of_status(value):
        for i, (val, _) in enumerate(Order.STATUS_CHOICES):
            if val == value:
                return i
        return None

    def clean(self):
        existing_order = Order.objects.get(id=self.id) if self.id else None
        if existing_order:
            new_index = Order.find_index_of_status(self.status)
            old_index = Order.find_index_of_status(existing_order.status)
            if new_index < old_index:
                raise ValidationError({'status': 'Can\'t revert to a previous status.'})
            if new_index == old_index:
                raise ValidationError({'status': 'Can\'t save the same status.'})
            if old_index + 1 != new_index:
                raise ValidationError({'status': 'Can\'t skip a status.'})

    def __str__(self):
        return f"{self.customer.username} - {self.status}"


class OrderItem(AbstractOrderItem):
    are_coupons_used = models.BooleanField(default=False, null=False)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    food_portion = models.ForeignKey(FoodPortion, on_delete=models.SET_NULL, null=True)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return f"{self.order.__str__()} - {self.food_portion.food.name}"


# Records
class OrderRecord(AbstractOrder):
    class Meta:
        verbose_name = "Order Record"
        verbose_name_plural = "Order Records"

    def __str__(self):
        return f"{self.customer.username} - {self.date_time_edited.strftime('%Y-%m-%d %H:%M:%S')}"


class OrderItemRecord(AbstractOrderItem):
    discount = models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    price = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
    coupons_used = models.IntegerField(null=True, default=0, validators=[MinValueValidator(0)])

    order = models.ForeignKey(OrderRecord, on_delete=models.SET_NULL, null=True)
    food_portion = models.ForeignKey(FoodPortionRecord, on_delete=models.SET_NULL, null=True)


class OrderItemToppingRecord(models.Model):
    topping = models.ForeignKey(ToppingRecord, null=True, on_delete=models.SET_NULL)
    order_item = models.ForeignKey(OrderItemRecord, null=True, on_delete=models.SET_NULL)
    price = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
