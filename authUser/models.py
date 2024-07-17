from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=65)

    customer = models.BooleanField(default=True)
    employee = models.BooleanField(default=False)
