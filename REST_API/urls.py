from django.urls import include, path
from rest_framework.routers import DefaultRouter

from REST_API import export_scripts
from REST_API.views import *

router = DefaultRouter()

router.register(r"parking_space", ParkingSpaceView, basename="parkingspace")
router.register(r"vehicle_info", Vehicle_infoView, basename="vehicleinfo")
# router.register(r'parking-details',ParkingDetailsView,basename='parking-details')

urlpatterns = [
    path("parking-details", ParkingDetailsView.as_view(), name="parking-details"),
    path(r"", include(router.urls)),
    path('export/', export_scripts.export_to_excel, name='export_to_excel'),
    path('upload-file-parking_space/', ParkingSpaceUploadView.as_view(),
         name='upload_csv_parking_space'),
    path('upload-file-vehicle_info/', VehicleInfoUploadView.as_view(),
         name='upload_csv_vehicle_info'),
    # path('upload-file-parking_details/', parkingdets.as_view(), name='upload_csv_'),

]
