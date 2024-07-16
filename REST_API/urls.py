from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()

router.register('parking_space',ParkingSpaceView,basename='parking-space')
router.register('vehicle_info',Vehicle_infoView,basename='vehicel-info')
router.register('parking-details',ParkingDetailsView,basename='parking-details')

urlpatterns = [
    
]+router.urls
