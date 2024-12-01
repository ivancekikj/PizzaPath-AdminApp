from django.db import models
from django.contrib.auth.models import User

class ExtraUserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    adress = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
