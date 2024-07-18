from django.db import models

from django.contrib.auth.models import AbstractUser,UserManager
from django.utils import timezone

class CustomUserManager(UserManager):
        def create_superuser(self,username, email=None,password=None, **extra_fields):
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
            extra_fields.setdefault("customer", False)
            if extra_fields.get("is_staff") is not True:
                raise ValueError("Superuser must have is_staff=True.")
            if extra_fields.get("is_superuser") is not True:
                raise ValueError("Superuser must have is_superuser=True.")
            return self._create_user( username,email,password, **extra_fields)
class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    customer = models.BooleanField(default=True)
    employee = models.BooleanField(default=False)
    objects = CustomUserManager()