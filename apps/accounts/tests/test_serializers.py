from django.test import TestCase

from apps.accounts.models import CouponReward, Customer, NewsletterPost
from apps.accounts.serializers import (
    CouponRewardSerializer,
    CustomerSerializer,
    NewsletterPostSerializer,
    RatingSerializer,
)
from apps.menu.models import Food, FoodPortion, Rating


class CouponRewardSerializerTests(TestCase):
    def test_serialize_coupon_reward(self):
        # given
        food_potion = FoodPortion(id=1, price=100, coupon_value=10, discount=0)
        coupon_reward = CouponReward(food_portion=food_potion, count=5)

        # when
        serializer = CouponRewardSerializer(coupon_reward)

        # then
        self.assertEqual(len(serializer.data.keys()), 2)


class CustomerSerializerTests(TestCase):
    def test_serialize_customer(self):
        # given
        customer = Customer(
            username="customer",
            email="customer@gmail.com",
            address="123 Street",
            phone_number="069/420-666",
            first_name="John",
            last_name="Doe",
            is_subscribed_to_newsletter=True,
            password="customer",
        )

        # when
        serializer = CustomerSerializer(customer)

        # then
        self.assertEqual(len(serializer.data.keys()), 8)


class RatingSerializerTests(TestCase):
    def test_serialize_rating(self):
        # given
        food = Food(id=1)
        rating = Rating(food=food, value=5)

        # when
        serializer = RatingSerializer(rating)

        # then
        self.assertEqual(len(serializer.data.keys()), 2)


class NewsletterPostSerializerTests(TestCase):
    def test_serialize_newsletter_post(self):
        # given
        post = NewsletterPost(title="Title", content="Content")

        # when
        serializer = NewsletterPostSerializer(post)

        # then
        self.assertEqual(len(serializer.data.keys()), 4)
