from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.menu.models import FoodPortion


class User(AbstractUser):
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
    phone_number = models.CharField(max_length=20, null=False)
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


class WorkingDay(models.Model):
    OPENING_TIME = "08:00"
    CLOSING_TIME = "16:00"
    NON_WORKING_DAYS = ("Saturday", "Sunday")

    date = models.DateField(null=False, blank=False)
    is_closed = models.BooleanField(default=False, blank=False, null=False)
    start_time = models.TimeField(null=True, blank=True, default=OPENING_TIME)
    end_time = models.TimeField(null=True, blank=True, default=CLOSING_TIME)

    class Meta:
        verbose_name = "Working Day"
        verbose_name_plural = "Working Days"

    def __str__(self):
        return self.date
