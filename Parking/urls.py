from django.urls import path
from .views import *
urlpatterns = [
    path('parking/',ParkingSpaceView),
    path('parkingSpace/info/<pk>/',ParkingSpaceInfoView),
    path('parkingSpace/change/<pk>/',ParkingSpaceChangeView),
    path('parkingSpace/delete/<pk>/',ParkingSpaceDeleteView),
    path('parkingSpace/create/',ParkingSpaceCreateView),

    path('vehicle_details/',VehicleDetailsView),
    path('vehicle_details/create/',VehicleDetailsAdd),
    path('vehicle_details/info/<pk>',VehicleDetailInfo),
    path('vehicle_details/edit/<pk>',VehicleDetailEdit),
    path('vehicle_details/delete/<pk>',VehicleDetailDelete),

    


]
