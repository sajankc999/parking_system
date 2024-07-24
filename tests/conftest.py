import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from factories import (
    ParkingDetailsFactory,
    ParkingSpaceFactory,
    UserFactory,
    VehicleInfoFactory,
)
from rest_framework import status
from rest_framework.test import APIClient

from REST_API.models import ParkingDetails, ParkingSpace, Vehicle_info

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def customer():
    return UserFactory()


@pytest.fixture
def superuser():
    return UserFactory(is_superuser=True)


@pytest.fixture
def employee():
    return UserFactory(is_staff=True, employee=True, is_active=True)


# @pytest.fixture

# @pytest.fixture
# @pytest.fixture

# @pytest.fixture
# def user_create():
