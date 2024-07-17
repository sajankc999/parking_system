from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.viewsets import ModelViewSet,ViewSet,generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .pagination import *
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters
from rest_framework.decorators import action
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
class ParkingDetailsView(generics.ListCreateAPIView):
    queryset=ParkingDetails.objects.all()
    serializer_class = ParkingDetailsSerializer
    pagination_class=ParkingDetailsPagination
    filter_backends=[DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['parking_space', 'vehicle_info']
    ordering_fields =['checkin_time','checkout_time']

    def update(self, request, *args, **kwargs):
        raise Response("method not allowed")
    
    def destroy(self, request, *args, **kwargs):
        return Response('method not allowed')
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = ParkingDetailsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            parking_space_id = data.get('parking_space')
            vehicle_info_id=data.get('vehicle_info')
            checkout_time=data.get('checkout_time')
            # raise Exception(parking_space,vehicle_info)
            vehicle_obj = Vehicle_info.objects.filter(pk=vehicle_info_id).first()
            parking_obj = ParkingSpace.objects.filter(pk=parking_space_id).first()
            
            parking=ParkingDetails.objects.filter(vehicle_info=vehicle_info_id).first()
            if parking:
                # ParkingDetails.objects.filter(vehicle_info=vehicle_info_id).first()
                # Check if parking.checkout_time is timezone-aware
                if parking.checkout_time > timezone.now():
                
                    parking.parking_space.occupied=True
                    parking.parking_space.save()
                    vehicle_obj.parked=True
                    vehicle_obj.save()
                else:
                    parking.parking_space.occupied=False
                    parking.parking_space.save()
                    vehicle_obj.parked=False
                    vehicle_obj.save()
                    # context['error']='Vehicle is already parked'
            
            if parking_obj.occupied:
                return Response('parking spot is occupied')
            else:
                ParkingDetails.objects.create(parking_space=parking_obj,
                                                vehicle_info=vehicle_obj,
                                            checkout_time=checkout_time)
                
                vehicle_obj.parked=True
                vehicle_obj.save()
                parking_obj.occupied=True
                parking_obj.save()
                return Response(status=status.HTTP_201_CREATED)
                # return render(request,'ParkingDetails.html',context)            
            
