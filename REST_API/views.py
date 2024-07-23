from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, generics

from REST_API.models import *
from REST_API.pagination import *
from REST_API.permissions import *
from REST_API.serializer import *

user = get_user_model()

"""model view for CRUD operation of parking space"""


class ParkingSpaceView(ModelViewSet):
    queryset = ParkingSpace.objects.all()
    serializer_class = ParkingSpaceSerializer
    pagination_class = ParkingSpacePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["occupied", "name", "number"]

    def create(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return Response('login required', status=status.HTTP_401_UNAUTHORIZED)
        if self.request.user.is_superuser or self.request.user.employee:
            return super().create(request, *args, **kwargs)
        else:
            return Response('Unauthorized', status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.employee:
            return super().update(request, *args, **kwargs)
        return Response('unauthorized', status=status.HTTP_403_FORBIDDEN
                        )

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.employee:
            return super().destroy(request, *args, **kwargs)
        return Response('unauthorized', status=status.HTTP_403_FORBIDDEN
                        )


"""modelviewset for CRUD operation of vehivle information"""


class Vehicle_infoView(ModelViewSet):

    serializer_class = Vehicle_infoSerializer
    permission_classes = [IsAuthenticated]

    pagination_class = VehicleInfoPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = ["type", "plate_no", "parked"]

    def get_queryset(self):
        user = self.request.user
        # raise Exception(user)
        if user.customer:
            return Vehicle_info.objects.filter(user=user)
        if user.is_staff or user.is_superuser:
            return Vehicle_info.objects.all()

    def create(self, request, *args, **kwargs):
        # raise Exception(self.request.user)
        user = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            # raise Exception(data)
            vehicle_info = Vehicle_info.objects.filter(
                plate_no=data["plate_no"]
            )
            if not vehicle_info:
                Vehicle_info.objects.create(**data)
                return Response("vehicle added", status=status.HTTP_201_CREATED)
            return Response(
                "vehicle already exists", status=status.HTTP_400_BAD_REQUEST
            )


"""class view for creating and listing parking details
 /// parked field in vehicel_info class and ocupied in parking space class is set to be true after creations"""


class ParkingDetailsView(generics.ListCreateAPIView):
    queryset = ParkingDetails.objects.all()
    serializer_class = ParkingDetailsSerializer
    pagination_class = ParkingDetailsPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["parking_space", "vehicle_info"]
    ordering_fields = ["checkin_time", "checkout_time"]

    def get_queryset(self):
        user = self.request.user
        if user.customer:
            return ParkingDetails.objects.filter(vehicle_info__user=user).order_by("created_at")
        if user.is_staff or user.is_superuser:
            return self.queryset
        return Response("something went wrong")

    def create(self, request, *args, **kwargs):
        data = request.data
        if request.user.is_superuser or request.user.employee:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                parking_space_id = data.get("parking_space")
                vehicle_info_id = data.get("vehicle_info")
                checkout_time = data.get("checkout_time")
                # raise Exception(parking_space,vehicle_info)
                vehicle_obj = Vehicle_info.objects.filter(
                    pk=vehicle_info_id).first()
                parking_obj = ParkingSpace.objects.filter(
                    pk=parking_space_id).first()

                parking = ParkingDetails.objects.filter(
                    vehicle_info=vehicle_info_id
                ).first()
                if parking:
                    # ParkingDetails.objects.filter(vehicle_info=vehicle_info_id).first()
                    # Check if parking.checkout_time is timezone-aware
                    if parking.checkout_time > timezone.now():

                        parking.parking_space.occupied = True
                        parking.parking_space.save()
                        vehicle_obj.parked = True
                        vehicle_obj.save()
                    else:
                        parking.parking_space.occupied = False
                        parking.parking_space.save()
                        vehicle_obj.parked = False
                        vehicle_obj.save()
                        # context['error']='Vehicle is already parked'

                if parking_obj.occupied:
                    return Response("parking spot is occupied", status=status.HTTP_400_BAD_REQUEST)
                else:
                    ParkingDetails.objects.create(
                        parking_space=parking_obj,
                        vehicle_info=vehicle_obj,
                        checkout_time=checkout_time,
                    )

                    vehicle_obj.parked = True
                    vehicle_obj.save()
                    parking_obj.occupied = True
                    parking_obj.save()
                    return Response(status=status.HTTP_201_CREATED)
                    # return render(request,'ParkingDetails.html',context)
            else:
                return Response('Bad data', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('you dont have permission', status=status.HTTP_403_FORBIDDEN)
