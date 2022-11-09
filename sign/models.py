from django.db import models
from django.contrib.auth.models import User


class NewUserOTP(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
