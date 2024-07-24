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


@pytest.mark.django_db
class TestParkingSpaceView:
    @pytest.fixture(autouse=True)
    def setup(self):
        #
        self.url = reverse("parkingspace-list")
        self.superuser = UserFactory(is_superuser=True)
        self.employee = UserFactory(is_staff=True, employee=True)
        self.customer = UserFactory()
        self.parking_space = ParkingSpaceFactory(
            name='par', number=1, rate=123)
        self.detail_url = lambda pk: reverse('parkingspace-detail', args=[pk])

    @pytest.mark.parametrize("user, expected_status_code", [
        ("superuser", status.HTTP_200_OK),
        ("employee", status.HTTP_200_OK),
        ("user", status.HTTP_200_OK),
    ])
    def test_list_parkingspace(self, client, superuser, employee, customer, user, expected_status_code):
        ParkingSpaceFactory.create_batch(2)
        test_user = ''
        if user == "superuser":
            test_user = superuser
        elif user == "employee":
            test_user = employee
        elif user == "customer":
            test_user = customer
        client.force_authenticate(user=test_user)
        response = client.get(self.url + '?ordering=number')

        assert response.status_code == expected_status_code
        if response.status_code == status.HTTP_200_OK:
            assert len(response.data) == 4

    @pytest.mark.parametrize("user, expected_status_code", [
        ("superuser", status.HTTP_201_CREATED),
        ("employee", status.HTTP_201_CREATED),
        ("customer", status.HTTP_403_FORBIDDEN),
    ])
    def test_create_parkingspace(self, user, client, superuser, employee, customer, expected_status_code):
        data = {"name": "Parking Space 1",
                "number": 1, "rate": 20, "occupied": False}
        test_user = ''
        if user == "superuser":
            test_user = superuser
        elif user == "employee":
            test_user = employee
        elif user == "customer":
            test_user = customer
        client.force_authenticate(user=test_user)
        response = client.post(self.url, data, format="json")

        assert response.status_code == expected_status_code

        if response.status_code == status.HTTP_201_CREATED:
            assert ParkingSpace.objects.count() == 2
            assert ParkingSpace.objects.get(
                id=response.data["id"]).name == data["name"]

    @pytest.mark.parametrize("user, expected_status_code", [
        ("superuser", status.HTTP_200_OK),
        ("employee", status.HTTP_200_OK),
        ("customer", status.HTTP_403_FORBIDDEN),
    ])
    def test_update_parkingspace(self, user, client, superuser, employee, customer, expected_status_code):
        parkingspace = ParkingSpaceFactory(
            name="Old Name", number=1, rate=20, occupied=False)
        data = {"name": "New Name", "number": 1, "rate": 20, "occupied": False}
        url = self.detail_url(parkingspace.id)
        # test_user = getattr(self, user)
        test_user = ''
        if user == "superuser":
            test_user = superuser
        elif user == "employee":
            test_user = employee
        elif user == "customer":
            test_user = customer
        client.force_authenticate(user=test_user)
        response = client.put(url, data, format="json")
        assert response.status_code == expected_status_code

        if response.status_code == status.HTTP_200_OK:
            parkingspace.refresh_from_db()
            assert parkingspace.name == data["name"]

    @pytest.mark.parametrize("user, expected_status_code", [
        ("superuser", status.HTTP_204_NO_CONTENT),
        ("employee", status.HTTP_204_NO_CONTENT),
        ("customer", status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_parkingspace(self, client, superuser, employee, customer, user, expected_status_code):
        parkingspace = ParkingSpaceFactory(
            name="Parking Space 1", number=1, rate=20, occupied=False)
        url = self.detail_url(parkingspace.id)
        # test_user = getattr(self, user)
        if user == "superuser":
            test_user = superuser
        elif user == "employee":
            test_user = employee
        elif user == "customer":
            test_user = customer
        client.force_authenticate(user=test_user)
        response = client.delete(url)
        assert response.status_code == expected_status_code

        if response.status_code == status.HTTP_204_NO_CONTENT:
            assert not ParkingSpace.objects.filter(id=parkingspace.id).exists()


@pytest.mark.django_db
class TestVehicleInfoView:
    @pytest.fixture(autouse=True)
    def set_up(self):

        self.url = reverse("vehicleinfo-list")
        self.user = UserFactory(
            is_superuser=False, is_staff=False, employee=False)
        self.user2 = UserFactory(
            is_superuser=False, is_staff=False, employee=False)
        self.superuser = UserFactory(is_superuser=True, is_staff=True)
        self.employee = User.objects.create_employee(
            username='user23', password='password123')
        self.vehicle_info1 = VehicleInfoFactory(user=self.user)
        self.vehicle_info2 = VehicleInfoFactory(user=self.user2)
        print(self.vehicle_info1.id, self.vehicle_info2.id)
        self.detail_url = lambda pk: reverse("vehicleinfo-detail", args=[pk])
        self.data = {"type": "bus", "plate_no": "444"}

    @pytest.mark.parametrize("user, expected_code,expected_results", [
        ("superuser", status.HTTP_200_OK, 2),
        ("employee", status.HTTP_200_OK, 2),
        ("user", status.HTTP_200_OK, 1),
    ])
    def test_retrieve_vehicleinfo(self, user, client, superuser, employee, customer, expected_code, expected_results):
        # vehicle_info1 = Vehicle_info.objects.create(
        # user=self.user, type='car', plate_no='123')
        # vehicle_info2 = Vehicle_info.objects.create(
        # user=self.user2, type='bike', plate_no='333')
        if user == "superuser":
            test_user = superuser
        elif user == "employee":
            test_user = employee
        elif user == "customer":
            test_user = customer
        print("hdfoasdhf:::::;::::::",
              Vehicle_info.objects.all().values('user__username'))

        client.force_authenticate(user=test_user)
        response = client.get(self.url)

        print("user::;;", type(user))
        # if test_user == "user":
        #     assert response.status_code == expected_code
        #     print(response.data)

        assert response.status_code == expected_code
        assert len(response.data['results']) == expected_results
        client.logout()

    @pytest.mark.parametrize("user, expected_status_code, expected_count", [
        ("user", status.HTTP_201_CREATED, 2),
        ("unauthenticated", status.HTTP_401_UNAUTHORIZED, None),
    ])
    def test_create_vehicleinfo(self, user, client, superuser, employee, customer, expected_status_code, expected_count):
        if user == "superuser":
            test_user = superuser
        elif user == "employee":
            test_user = employee
        elif user == "customer":
            test_user = customer
        if test_user:
            client.force_authenticate(user=test_user)
        else:
            client.logout()

        response = client.post(self.url, self.data, format='json')
        assert response.status_code == expected_status_code

        if expected_count is not None:
            assert Vehicle_info.objects.filter(
                user=self.user).count() == expected_count

    @pytest.mark.parametrize("user, detail_url, update_status_code, delete_status_code, expected_plate_no", [
        ("user", None, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, "444"),
        ("superuser", None, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, "444"),
        # ("unauthenticated", None, status.HTTP_401_UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED, None),
    ])
    def test_update_and_delete(self, user, client, superuser, employee, customer, detail_url, update_status_code, delete_status_code, expected_plate_no):
        if user == "superuser":
            test_user = superuser
        elif user == "employee":
            test_user = employee
        elif user == "customer":
            test_user = customer
        if test_user:
            client.force_authenticate(user=test_user)
        else:
            client.logout()

        if detail_url is None:
            detail_url = self.detail_url(self.vehicle_info1.id)

        response = client.put(detail_url, self.data, format='json')
        assert response.status_code == update_status_code

        if update_status_code == status.HTTP_200_OK:
            Vehicle_info.objects.get(
                id=self.vehicle_info1.id).refresh_from_db()
            assert Vehicle_info.objects.get(
                id=self.vehicle_info1.id).plate_no == expected_plate_no

        response = client.delete(detail_url)
        assert response.status_code == delete_status_code

        if delete_status_code == status.HTTP_204_NO_CONTENT:
            assert not Vehicle_info.objects.filter(
                id=self.vehicle_info1.id).exists()


@pytest.mark.django_db
class TestParkingDetailsView:
    @pytest.fixture(autouse=True)
    def set_up(self):

        self.url = reverse('parking-details')
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.superuser = UserFactory(is_superuser=True)
        self.employee = UserFactory(is_staff=True, employee=True)
        self.parking_space = ParkingSpaceFactory(
            name="Parking Space", number=10, occupied=False, rate=123)
        self.parking_space2 = ParkingSpaceFactory(
            name="Parking Space", number=1, occupied=False, rate=123)
        self.vehicle_info = VehicleInfoFactory(
            user=self.user, type="Car", plate_no="ABC123", parked=False)
        self.vehicle_info2 = VehicleInfoFactory(
            user=self.user2, type="Car", plate_no="ABC1234", parked=False)
        self.parking_details = ParkingDetailsFactory(
            parking_space=self.parking_space, vehicle_info=self.vehicle_info, checkout_time="2024-11-11T11:11:00Z")
        self.parking_details2 = ParkingDetailsFactory(
            parking_space=self.parking_space2, vehicle_info=self.vehicle_info2, checkout_time="2024-11-11T11:11:00Z")

    @pytest.mark.parametrize("user, expected_status_code, expected_count", [
        ("user", status.HTTP_200_OK, 1),
        ("employee", status.HTTP_200_OK, 2),
        ("superuser", status.HTTP_200_OK, 2),
    ])
    def test_list_parkingdetails(self, user, client, superuser, employee, customer, expected_status_code, expected_count):

        if user == "superuser":
            test_user = superuser
        elif user == "employee":
            test_user = employee
        elif user == "customer":
            test_user = customer
        client.force_authenticate(user=test_user)

        response = client.get(self.url)
        assert response.status_code == expected_status_code
        assert len(response.data['results']) == expected_count

    @pytest.mark.parametrize("user, expected_status_code, expected_count, expected_occupied, expected_parked, should_fail", [
        ("employee", status.HTTP_201_CREATED, 3, True, True, False),
        ("user", status.HTTP_403_FORBIDDEN, 2, False, False, True),
        ("employee", status.HTTP_400_BAD_REQUEST, 2, True, False, True),
    ])
    def test_create_parkingdetails(self, user, client, superuser, employee, customer, expected_status_code, expected_count, expected_occupied, expected_parked, should_fail):
        if user == "superuser":
            test_user = superuser
        elif user == "employee":
            test_user = employee
        elif user == "customer":
            test_user = customer

        if should_fail:
            self.parking_space.occupied = True
            self.parking_space.save()
        client.force_authenticate(user=test_user)
        data = {"parking_space": self.parking_space.id,
                "vehicle_info": self.vehicle_info.id, "checkout_time": "2024-12-31T23:59:59Z"}
        response = client.post(self.url, data, format='json')
        assert response.status_code == expected_status_code
        assert ParkingDetails.objects.count() == expected_count

        if not should_fail:
            self.parking_space.refresh_from_db()
            assert self.parking_space.occupied == expected_occupied
            self.vehicle_info.refresh_from_db()
            assert self.vehicle_info.parked == expected_parked

    # @pytest.mark.parametrize("user, parking_space_occupied, expected_status_code, expected_count, expected_error", [
    #     ("employee", True, status.HTTP_400_BAD_REQUEST, 2, "parking spot is occupied"),
    #     ("employee", False, status.HTTP_201_CREATED, 3, ""),
    # ])
    # def test_create_parkingdetails_with_occupied_space(self, user, client,superuser,employee,customer,parking_space_occupied, expected_status_code, expected_count, expected_error):
    #     client.force_authenticate(user=self.employee)
    #     self.parking_space.occupied = parking_space_occupied
    #     self.parking_space.save()

    #     data = {"parking_space": self.parking_space.id, "vehicle_info": self.vehicle_info.id, "checkout_time": "2024-12-31T23:59:59Z"}
    #     response = client.post(self.url, data, format='json')
    #     assert response.status_code == expected_status_code
    #     assert ParkingDetails.objects.count() == expected_count
    #     if expected_error:
    #         assert expected_error in str(response.data)
