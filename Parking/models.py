from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
import uuid

class ParkingSpace(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(validators=(MinValueValidator(0),MaxValueValidator(10)))
    rate = models.IntegerField()
    occupied=models.BooleanField(default=False)
    def __str__(self) -> str:
        return f'{self.name}{self.number}'
    
class Vehicle_info(models.Model):
    type = models.CharField(max_length=100)
    plate_no = models.CharField(max_length=10)
    
    

class ParkingDetails(models.Model):
    parking_space = models.ForeignKey(ParkingSpace,on_delete=models.CASCADE)
    vehicle_info = models.ForeignKey(Vehicle_info,on_delete=models.CASCADE)
    token = models.CharField(default=uuid.uuid4,max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    checkin_time = models.DateTimeField(auto_now=True)
    checkout_time = models.DateTimeField()