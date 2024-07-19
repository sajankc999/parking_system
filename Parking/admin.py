from django.contrib import admin

# Register your models here.
from Parking.models import ParkingSpace,ParkingDetails,Vehicle_info

admin.site.register(ParkingSpace)
admin.site.register(Vehicle_info)
admin.site.register(ParkingDetails)
