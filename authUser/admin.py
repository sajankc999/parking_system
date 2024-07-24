from django.contrib import admin

from .models import *
from import_export.admin import ImportExportModelAdmin
from REST_API.resources import UserResource
# Register your models here.


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
