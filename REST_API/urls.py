from django.urls import include, path
from rest_framework.routers import DefaultRouter

from REST_API.views import *

router = DefaultRouter()

router.register(r"parking_space", ParkingSpaceView, basename="parking-space")
router.register(r"vehicle_info", Vehicle_infoView, basename="vehicel-info")
# router.register(r'parking-details',ParkingDetailsView,basename='parking-details')

urlpatterns = [
    path("parking-details", ParkingDetailsView.as_view(), name="parking-details"),
    path("", include(router.urls)),
]
