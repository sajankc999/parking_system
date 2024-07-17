from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(ParkingDetails)
admin.site.register(ParkingSpace)
admin.site.register(Vehicle_info)