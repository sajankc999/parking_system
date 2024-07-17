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
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import get_user_model
from .permissions import *

user = get_user_model()

"""model view for CRUD operation of parking space"""
class ParkingSpaceView(ModelViewSet):
    queryset = ParkingSpace.objects.all()
    serializer_class=ParkingSpaceSerializer
    pagination_class = ParkingSpacePagination
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['occupied', 'name','number']


    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsCustomer | IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsEmployee | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    



"""modelviewset for CRUD operation of vehivle information"""
class Vehicle_infoView(ModelViewSet):
    queryset = Vehicle_info.objects.all()
    serializer_class = Vehicle_infoSerializer
    permission_classes = [IsAuthenticated]

    pagination_class=VehicleInfoPagination
    filter_backends=[DjangoFilterBackend,]
    filterset_fields = ['type', 'plate_no','parked']


"""class view for creating and listing parking details
 /// parked field in vehicel_info class and ocupied in parking space class is set to be true after creations"""
class ParkingDetailsView(generics.ListCreateAPIView):
    queryset=ParkingDetails.objects.all()
    serializer_class = ParkingDetailsSerializer
    pagination_class=ParkingDetailsPagination
    filter_backends=[DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['parking_space', 'vehicle_info']
    ordering_fields =['checkin_time','checkout_time']


    
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
            
