from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.menu.models import AbstractCategory, AbstractFood, AbstractRating, AbstractSize, AbstractTopping
from apps.orders.models import AbstractOrder


class CategoryRecord(AbstractCategory):
    pass


class SizeRecord(AbstractSize):
    pass


class ToppingRecord(AbstractTopping):
    pass


class FoodRecord(AbstractFood):
    image = models.ImageField(upload_to="food_record_photos")
    category = models.ForeignKey(CategoryRecord, null=True, blank=False, on_delete=models.SET_NULL)


class RatingRecord(AbstractRating):
    food = models.ForeignKey(FoodRecord, on_delete=models.SET_NULL, null=True)


class FoodPortionRecord(models.Model):
    size = models.ForeignKey(SizeRecord, null=True, blank=False, on_delete=models.SET_NULL)
    food = models.ForeignKey(FoodRecord, null=True, blank=False, on_delete=models.SET_NULL)


class OrderRecord(AbstractOrder):
    pass


class OrderItemRecord(AbstractOrder):
    discount = models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    price = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
    coupons_used = models.IntegerField(null=True, default=0, validators=[MinValueValidator(0)])

    order = models.ForeignKey(OrderRecord, on_delete=models.SET_NULL, null=True)
    food_portion = models.ForeignKey(FoodPortionRecord, on_delete=models.SET_NULL, null=True)


class OrderItemToppingRecord(models.Model):
    topping = models.ForeignKey(ToppingRecord, null=True, on_delete=models.SET_NULL)
    order_item = models.ForeignKey(OrderItemRecord, null=True, on_delete=models.SET_NULL)
    price = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])