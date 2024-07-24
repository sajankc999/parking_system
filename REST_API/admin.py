from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from REST_API.models import *
from REST_API.models import ParkingSpace
from REST_API.resources import ParkingSpaceResource, ParkingDetailsResource, VehicleInfoResource


@admin.register(ParkingSpace)
class ParkingSpaceAdmin(ImportExportModelAdmin):
    resource_class = ParkingSpaceResource


@admin.register(ParkingDetails)
class ParkingDetailsAdmin(ImportExportModelAdmin):
    resource_class = ParkingDetailsResource
# admin.site.register(ParkingSpace,ParkingSpaceAdmin)


@admin.register(Vehicle_info)
class VehicleInfoAdmin(ImportExportModelAdmin):
    resource_class = VehicleInfoResource
