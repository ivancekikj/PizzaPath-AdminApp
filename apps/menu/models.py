from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class AbstractCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class AbstractTopping(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        abstract = True


class AbstractFood(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    class Meta:
        abstract = True


class AbstractSize(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractRating(models.Model):
    value = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    customer = models.ForeignKey("accounts.Customer", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class Category(AbstractCategory):
    pass


class Topping(AbstractTopping):
    price = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class Food(AbstractFood):
    image = models.ImageField(upload_to="food_photos")

    category = models.ForeignKey(Category, null=True, blank=False, on_delete=models.SET_NULL)
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return self.name


class Size(AbstractSize):
    pass


class FoodPortion(models.Model):
    price = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
    discount = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    coupon_value = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])

    size = models.ForeignKey(Size, null=True, blank=False, on_delete=models.SET_NULL)
    food = models.ForeignKey(Food, null=True, blank=False, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Food Portion"
        verbose_name_plural = "Food Portions"

    def __str__(self):
        return f"{self.food.name} - {self.size.name}"


class Rating(AbstractRating):
    food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.customer.username} - {self.food.name}"


# Records
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
