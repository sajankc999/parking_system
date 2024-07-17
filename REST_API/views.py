from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT
from .pagination import *
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters

class ParkingSpaceView(ModelViewSet):
    queryset = ParkingSpace.objects.all()
    serializer_class=ParkingSpaceSerializer
    pagination_class = ParkingSpacePagination
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['occupied', 'name','number']

class Vehicle_infoView(ModelViewSet):
    queryset = Vehicle_info.objects.all()
    serializer_class = Vehicle_infoSerializer
    pagination_class=VehicleInfoPagination
    filter_backends=[DjangoFilterBackend,]
    filterset_fields = ['type', 'plate_no','parked']
class ParkingDetailsView(ModelViewSet):
    queryset=ParkingDetails.objects.all()
    serializer_class = ParkingDetailsSerializer
    pagination_class=ParkingDetailsPagination
    filter_backends=[DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['parking_space', 'vehicle_info']
    ordering_fields =['checkin_time','checkout_time']