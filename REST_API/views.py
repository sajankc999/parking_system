from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT
from .pagination import *
class ParkingSpaceView(ModelViewSet):
    queryset = ParkingSpace.objects.all()
    serializer_class=ParkingSpaceSerializer
    pagination_class = ParkingSpacePagination


class Vehicle_infoView(ModelViewSet):
    queryset = Vehicle_info.objects.all()
    serializer_class = Vehicle_infoSerializer
    pagination_class=VehicleInfoPagination
class ParkingDetailsView(ModelViewSet):
    queryset=ParkingDetails.objects.all()
    serializer_class = ParkingDetailsSerializer
    pagination_class=ParkingDetailsPagination