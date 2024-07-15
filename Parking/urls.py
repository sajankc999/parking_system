from django.urls import path
from .views import *
urlpatterns = [
    path('parking/',ParkingSpaceView),
    path('parkingSpace/info/<pk>/',ParkingSpaceInfoView),
    path('parkingSpace/change/<pk>/',ParkingSpaceChangeView),
    path('parkingSpace/delete/<pk>/',ParkingSpaceDeleteView),
    path('parkingSpace/create/',ParkingSpaceCreateView),
]
