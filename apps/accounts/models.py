from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

from apps.menu.models import FoodPortion


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_email_confirmed = models.BooleanField(default=False, null=False)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.username


class NewsletterPost(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = "Newsletter Post"
        verbose_name_plural = "Newsletter Posts"

    def __str__(self):
        return self.title


class Customer(User):
    address = models.CharField(max_length=200, null=False)
    phone_number = models.CharField(max_length=20, null=False, unique=True)
    is_subscribed_to_newsletter = models.BooleanField(default=False, null=False)

    received_posts = models.ManyToManyField(NewsletterPost)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.username


class CouponReward(models.Model):
    count = models.IntegerField(null=False, default=0, validators=[MinValueValidator(0)])

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    food_portion = models.ForeignKey(FoodPortion, on_delete=models.SET_NULL, null=True)
