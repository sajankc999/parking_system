from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
import uuid
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

user = get_user_model()
"""model to store information of the parking loctaion"""
class ParkingSpace(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(validators=(MinValueValidator(0),MaxValueValidator(10)))
    rate = models.IntegerField()
    occupied=models.BooleanField(default=False)
    def __str__(self) -> str:
        return f'{self.name}{self.number}'
    

"""
    model for storing vehicle information .
    parked field is to show the vehicle is parked or not
"""
class Vehicle_info(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    plate_no = models.CharField(max_length=10)
    parked = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.plate_no
    
"""it stores the relation of vehicle of parking spot """
class ParkingDetails(models.Model):
    parking_space = models.ForeignKey(ParkingSpace,on_delete=models.CASCADE)
    vehicle_info = models.ForeignKey(Vehicle_info,on_delete=models.CASCADE)
    token = models.CharField(default=uuid.uuid4,max_length=100)
    created_at = models.DateTimeField(default=timezone.now,editable=False)
    checkin_time = models.DateTimeField(default=timezone.now,null=True,blank=True)
    checkout_time = models.DateTimeField()