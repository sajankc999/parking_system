from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from REST_API.models import *
from REST_API.models import ParkingSpace
from REST_API.resources import ParkingSpaceResourse


@admin.register(ParkingSpace)
class ParkingSpaceAdmin(ImportExportModelAdmin):
    resource_class = ParkingSpaceResourse


admin.site.register(ParkingDetails)
# admin.site.register(ParkingSpace,ParkingSpaceAdmin)
admin.site.register(Vehicle_info)
