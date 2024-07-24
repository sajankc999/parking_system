import uuid

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory.django import DjangoModelFactory

from REST_API.models import ParkingDetails, ParkingSpace, Vehicle_info

User = get_user_model()


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class ParkingSpaceFactory(DjangoModelFactory):
    class Meta:
        model = ParkingSpace

    name = factory.Sequence(lambda n: f'Parking Space {n}')
    # Ensures number is between 1 and 10
    number = factory.Iterator(range(1, 11))
    rate = factory.Faker('random_int', min=1, max=500)
    occupied = factory.Faker('boolean')


class VehicleInfoFactory(DjangoModelFactory):
    class Meta:
        model = Vehicle_info

    user = factory.SubFactory(UserFactory)
    type = factory.Faker('word')
    plate_no = factory.Sequence(lambda n: f'{n:03}')
    parked = factory.Faker('boolean')


class ParkingDetailsFactory(DjangoModelFactory):
    class Meta:
        model = ParkingDetails

    parking_space = factory.SubFactory(ParkingSpaceFactory)
    vehicle_info = factory.SubFactory(VehicleInfoFactory)
    token = factory.LazyAttribute(lambda _: str(uuid.uuid4()))
    created_at = factory.LazyFunction(timezone.now)
    checkin_time = factory.LazyAttribute(
        lambda _: timezone.now() if timezone.now() else None)
    checkout_time = factory.Faker('date_time_this_year')
