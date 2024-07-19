# Create your models here.
import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
from django.db import models
from django.utils import timezone

user = get_user_model()


"""
    Class ParkingSpace.
    occupied fields siginifies the occupancy

"""


class ParkingSpace(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(
        validators=(MinValueValidator(0), MaxValueValidator(10))
    )
    rate = models.IntegerField()
    occupied = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}{self.number}"


"""
    Model for storing vehicle information .
    parked field is to show the vehicle is parked or not

"""


class Vehicle_info(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    plate_no = models.CharField(max_length=10)
    parked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.plate_no


"""
    ParkingDeatils model for sotring relation .
    parking space and vehicle info is related here
"""


class ParkingDetails(models.Model):
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE) #noqa skips the 
    vehicle_info = models.ForeignKey(Vehicle_info, on_delete=models.CASCADE)
    token = models.CharField(default=uuid.uuid4, max_length=100)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    checkin_time = models.DateTimeField(
        default=timezone.now, null=True, blank=True)
    checkout_time = models.DateTimeField()
