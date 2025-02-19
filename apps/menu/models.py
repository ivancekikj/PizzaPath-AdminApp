from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to="food_photos")
    description = models.TextField(blank=False, null=False)

    category = models.ForeignKey(Category, null=True, blank=False, on_delete=models.SET_NULL)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class FoodPortion(models.Model):
    price = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
    discount = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    coupon_value = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True, blank=False, null=False)

    size = models.ForeignKey(Size, null=True, blank=False, on_delete=models.SET_NULL)
    food = models.ForeignKey(Food, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.food.name} - {self.size.name}"


class Rating(models.Model):
    value = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(5)])

    customer = models.ForeignKey("accounts.Customer", on_delete=models.SET_NULL, null=True)
    food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.customer.username} - {self.food.name}"
