from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.viewsets import ModelViewSet

class ParkingSpaceView(ModelViewSet):
    queryset = ParkingSpace.objects.all()
    serializer_class = ParkingSpaceSerializer


class Vehicle_infoView(ModelViewSet):
    queryset = Vehicle_info.objects.all()
    serializer_class = Vehicle_infoSerializer

class ParkingDetailsView(ModelViewSet):
    queryset = ParkingDetails.objects.all()
    serializer_class = ParkingDetailsSerializer
