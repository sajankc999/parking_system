from import_export import resources

from REST_API.models import ParkingSpace, Vehicle_info, ParkingDetails
from django.contrib.auth import get_user_model

User = get_user_model()


class ParkingSpaceResource(resources.ModelResource):

    class Meta:
        model = ParkingSpace
        fields = ['id', 'name', 'number', 'rate', 'occupied']
        skip_unchanged = True
        use_bulk = True


class VehicleInfoResource(resources.ModelResource):
    class Meta:
        model = Vehicle_info
        fields = ['id', 'user', 'type', 'plate_no', 'parked']
        skip_unchanged = True
        use_bulk = True


class ParkingDetailsResource(resources.ModelResource):
    class Meta:
        model = ParkingDetails
        fields = ['id', 'parking_space', 'vehicle_info', 'token',
                  'created_at', 'checkin_time', 'checkout_time']
        skip_unchanged = True
        use_bulk = True


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = [
            'id',
            'username', 'first_name', 'last_name',
            'email', 'is_staff', 'is_active', 'date_joined',
            'customer', 'employee'
        ]
        skip_unchanged = True
        use_bulk = True
