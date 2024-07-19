from django.contrib import admin

# Register your models here.
from REST_API.models import *

admin.site.register(ParkingDetails)
admin.site.register(ParkingSpace)
admin.site.register(Vehicle_info)
