from django.urls import path
from .views import *
urlpatterns = [
    path('parking/',ParkingSpaceView,name='parking'),
    path('parkingSpace/info/<pk>/',ParkingSpaceInfoView,name="parking_space_info"),
    path('parkingSpace/change/<pk>/',ParkingSpaceChangeView,name="parking_space_edit"),
    path('parkingSpace/delete/<pk>/',ParkingSpaceDeleteView,name="parking_space_delete"),
    path('parkingSpace/create/',ParkingSpaceCreateView,name="parking_space_create"),

    path('vehicle_details/',VehicleDetailsView,name="vehicle_name"),
    path('vehicle_details/create/',VehicleDetailsAdd,name="vehicle_name_create"),
    path('vehicle_details/info/<pk>',VehicleDetailInfo,name="vehicle_name_info"),
    path('vehicle_details/edit/<pk>',VehicleDetailEdit,name="vehicle_name_edit"),
    path('vehicle_details/delete/<pk>',VehicleDetailDelete,name="vehicle_name_delete"),

    path('parking-details/',parking_details,name='parking-details'),

    path('',home,name='home')

]
