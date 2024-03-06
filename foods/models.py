from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    priceMKD = models.IntegerField()
    image = models.ImageField(upload_to="food_photos")

    def __str__(self):
        return self.name