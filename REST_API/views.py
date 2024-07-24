from tablib import Dataset
from django.core.files.storage import default_storage
import pandas as pd
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, generics

from REST_API.models import *
from REST_API.pagination import *
from REST_API.permissions import *
from REST_API.resources import ParkingSpaceResource, VehicleInfoResource, UserResource, ParkingDetailsResource
from REST_API.serializer import *

user = get_user_model()

"""model view for CRUD operation of parking space"""


class ParkingSpaceView(ModelViewSet):
    queryset = ParkingSpace.objects.all().order_by('pk')
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
        if not user.is_anonymous:
            if user.employee or user.is_superuser:
                return Vehicle_info.objects.all().order_by('-pk')

            return Vehicle_info.objects.filter(user=user).order_by('-pk')

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            if user.is_staff or user.is_superuser:
                return self.queryset

            return ParkingDetails.objects.filter(vehicle_info__user=user)

    def create(self, request, *args, **kwargs):
        data = request.data

        if not user.is_anonymous and request.user.is_superuser or request.user.employee:
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
                    return Response("Created successfully", status=status.HTTP_201_CREATED)
                    # return render(request,'ParkingDetails.html',context)
            else:
                return Response('Bad data', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('you dont have permission', status=status.HTTP_403_FORBIDDEN)


class ParkingSpaceUploadView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Save the uploaded file temporarily
            uploaded_file = serializer.validated_data['file']
            file_path = default_storage.save(uploaded_file.name, uploaded_file)

            try:
                # Determine the file type
                if file_path.endswith('.csv'):
                    # Read CSV file using pandas
                    df = pd.read_csv(default_storage.path(file_path))
                elif file_path.endswith('.xls'):
                    # Read XLS file using pandas
                    df = pd.read_excel(default_storage.path(
                        file_path), engine='xlrd')
                elif file_path.endswith('.xlsx'):
                    # Read XLSX file using pandas
                    df = pd.read_excel(default_storage.path(
                        file_path), engine='openpyxl')
                else:
                    return Response({'error': 'Unsupported file type. Please upload a CSV or Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

                # Convert the DataFrame to a list of dictionaries
                data = df.to_dict(orient='records')

                # Use the model resource to import the data
                resource = ParkingSpaceResource()

                # Create a Dataset from the data
                dataset = Dataset()
                dataset.dict = data

                result = resource.import_data(dataset, dry_run=False)

                # Check for import errors
                if result.has_errors():
                    errors = []
                    for row in result.rows:
                        if row.errors:
                            errors.append(
                                {'row': row.number, 'errors': row.errors})
                    return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

                return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            finally:
                # Delete the temporary file
                default_storage.delete(file_path)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleInfoUploadView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Save the uploaded file temporarily
            uploaded_file = serializer.validated_data['file']
            file_path = default_storage.save(uploaded_file.name, uploaded_file)

            try:
                # Determine the file type
                if file_path.endswith('.csv'):
                    # Read CSV file using pandas
                    df = pd.read_csv(default_storage.path(file_path))
                elif file_path.endswith('.xls'):
                    # Read XLS file using pandas
                    df = pd.read_excel(default_storage.path(
                        file_path), engine='xlrd')
                elif file_path.endswith('.xlsx'):
                    # Read XLSX file using pandas
                    df = pd.read_excel(default_storage.path(
                        file_path), engine='openpyxl')
                else:
                    return Response({'error': 'Unsupported file type. Please upload a CSV or Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

                # Convert the DataFrame to a list of dictionaries
                data = df.to_dict(orient='records')

                # Use the model resource to import the data
                resource = VehicleInfoResource()

                # Create a Dataset from the data
                dataset = Dataset()
                dataset.dict = data

                result = resource.import_data(dataset, dry_run=False)

                # Check for import errors
                if result.has_errors():
                    errors = []
                    for row in result.rows:
                        if row.errors:
                            errors.append(
                                {'row': row.number, 'errors': row.errors})
                    return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

                return Response({'message': 'Data imported successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            finally:
                # Delete the temporary file
                default_storage.delete(file_path)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
