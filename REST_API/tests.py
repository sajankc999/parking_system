import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from REST_API.models import ParkingDetails, ParkingSpace, Vehicle_info

User = get_user_model()


@pytest.mark.django_db
class TestParkingSpaceView:
    """
    Test suite for the ParkingSpace model API.

    This class contains tests to verify the functionality of
    the ParkingSpace API, including listing, creating, updating,
    and deleting parking spaces.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Setup method that runs before each test.

        This method initializes the API client, creates test users,
        and sets up test data including a ParkingSpace instance.
        """
        self.url = reverse("parkingspace-list")
        self.superuser = User.objects.create_superuser(
            username="admin", password="admin123")
        self.employee = User.objects.create_employee(
            username="employee", password="password123", is_staff=True)
        self.customer = User.objects.create_user(
            username="user1", password="password123")
        self.parking_space = ParkingSpace.objects.create(
            name='par', number=1, rate=123)
        self.detail_url = reverse(
            'parkingspace-list', args=[self.parking_space.id])
        self.client = APIClient()

    @pytest.mark.parametrize("user, expected_status_code", [
        ("superuser", status.HTTP_200_OK),
        ("employee", status.HTTP_200_OK),
        ("customer", status.HTTP_200_OK),
    ])
    def test_list_parkingspace(self, user, expected_status_code):
        """
        Test listing of parking spaces.

        This test verifies that users with different roles can
        access the list of parking spaces.
        """
        # Create some parking spaces to be listed
        ParkingSpace.objects.create(
            name="Parking Space 1", number=1, rate=20, occupied=False)
        ParkingSpace.objects.create(
            name="Parking Space 2", number=2, rate=30, occupied=True)

        if user == "superuser":
            test_user = self.superuser
        elif user == "employee":
            test_user = self.employee
        elif user == "customer":
            test_user = self.customer
        self.client.force_authenticate(user=test_user)
        response = self.client.get(self.url + '?ordering=number')

        if response.status_code == expected_status_code:
            # Check if two parking spaces are listed
            assert len(response.data) == 4

    @pytest.mark.parametrize("user, expected_status_code", [
        ("superuser", status.HTTP_201_CREATED),
        ("employee", status.HTTP_201_CREATED),
        ("customer", status.HTTP_403_FORBIDDEN),
    ])
    def test_create_parkingspace(self, user, expected_status_code):
        """
        Test creation of a parking space.

        This test ensures that superusers and employees can create
        a parking space, while customers cannot.
        """
        data = {"name": "Parking Space 1",
                "number": 1, "rate": 20, "occupied": False}

        if user == "superuser":
            test_user = self.superuser
        elif user == "employee":
            test_user = self.employee
        elif user == "customer":
            test_user = self.customer

        self.client.force_authenticate(user=test_user)
        response = self.client.post(self.url, data, format="json")
        print("USER:::", test_user)
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
    def test_update_parkingspace(self, user, expected_status_code):
        """
        Test updating a parking space.

        This test checks if superusers and employees can update
        parking space details, while customers are forbidden.
        """
        parkingspace = ParkingSpace.objects.create(
            name="Old Name", number=1, rate=20, occupied=False)
        data = {"name": "New Name", "number": 1, "rate": 20, "occupied": False}
        url = reverse("parkingspace-detail", args=[parkingspace.id])

        if user == "superuser":
            test_user = self.superuser
        elif user == "employee":
            test_user = self.employee
        elif user == "customer":
            test_user = self.customer

        self.client.force_authenticate(user=test_user)
        response = self.client.put(url, data, format="json")
        assert response.status_code == expected_status_code

        if response.status_code == status.HTTP_200_OK:
            parkingspace.refresh_from_db()
            assert parkingspace.name == data["name"]

    @pytest.mark.parametrize("user, expected_status_code", [
        ("superuser", status.HTTP_204_NO_CONTENT),
        ("employee", status.HTTP_204_NO_CONTENT),
        ("customer", status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_parkingspace(self, user, expected_status_code):
        """
        Test deleting a parking space.

        This test ensures that only superusers and employees can delete
        parking spaces, while customers are forbidden.
        """
        parkingspace = ParkingSpace.objects.create(
            name="Parking Space 1", number=1, rate=20, occupied=False)
        url = reverse("parkingspace-detail", args=[parkingspace.id])

        if user == "superuser":
            test_user = self.superuser
        elif user == "employee":
            test_user = self.employee
        elif user == "customer":
            test_user = self.customer

        self.client.force_authenticate(user=test_user)
        response = self.client.delete(url)
        assert response.status_code == expected_status_code

        if response.status_code == status.HTTP_204_NO_CONTENT:
            assert not ParkingSpace.objects.filter(id=parkingspace.id).exists()


@pytest.mark.django_db
class TestVehicleInfoView:
    """
    Test suite for the VehicleInfo model API.

    This class contains tests to verify the functionality of
    the VehicleInfo API, including retrieving, creating, updating,
    and deleting vehicle information.
    """

    @pytest.fixture(autouse=True)
    def set_up(self):
        """
        Setup method that runs before each test.

        This method initializes the API client, creates test users,
        and sets up test data including VehicleInfo instances.
        """
        self.client = APIClient()
        self.url = reverse("vehicleinfo-list")
        self.user = User.objects.create_user(
            username="user1", password="password123")
        self.user2 = User.objects.create_user(
            username="user2", password="password123")
        self.superuser = User.objects.create_superuser(
            username="admin", password="admin123")
        self.employee = User.objects.create_user(
            username="employee", password="password123", is_staff=True)
        self.vehicle_info1 = Vehicle_info.objects.create(
            user=self.user, type='car', plate_no='123')
        self.vehicle_info2 = Vehicle_info.objects.create(
            user=self.user2, type='bike', plate_no='333')
        self.detail_url = lambda pk: reverse("vehicleinfo-detail", args=[pk])
        self.data = {"type": "bus", "plate_no": "444"}

    @pytest.mark.parametrize("user, expected_code", [
        ("superuser", status.HTTP_200_OK),
        ("employee", status.HTTP_200_OK),
        ("user", status.HTTP_200_OK),
    ])
    def test_retrieve_vehicleinfo(self, user, expected_code):
        """
        Test retrieving vehicle information.

        This test verifies that different users can retrieve
        vehicle information according to their roles.
        """
        # Without login
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        test_user = {
            "superuser": self.superuser,
            "employee": self.employee,
            "user": self.user,
        }[user]

        # With login
        self.client.force_authenticate(user=test_user)
        response = self.client.get(self.url)

        if user == "user":
            assert response.status_code == expected_code
            assert len(response.data['results']) == 1

        assert response.status_code == expected_code
        self.client.logout()

        # Admin and staff can retrieve all
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url)
        assert len(response.data['results']) == 2

    @pytest.mark.parametrize("user, expected_status_code, expected_count", [
        ("user", status.HTTP_201_CREATED, 2),
        ("unauthenticated", status.HTTP_401_UNAUTHORIZED, None),
    ])
    def test_create_vehicleinfo(self, user, expected_status_code, expected_count):
        """
        Test creation of vehicle information.

        This test ensures that authenticated users can create
        vehicle information, while unauthenticated users cannot.
        """
        test_user = {
            "user": self.user,
            "unauthenticated": None
        }.get(user)

        if test_user:
            self.client.force_authenticate(user=test_user)
        else:
            self.client.logout()

        response = self.client.post(self.url, self.data, format='json')
        assert response.status_code == expected_status_code

        if expected_count is not None:
            assert Vehicle_info.objects.filter(
                user=self.user).count() == expected_count

        if expected_status_code == status.HTTP_400_BAD_REQUEST:
            assert "vehicle already exists" in str(response.data)

    @pytest.mark.parametrize("user, detail_url, update_status_code, delete_status_code, expected_plate_no", [
        ("user", None, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, "444"),
        ("superuser", None, status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, "444"),
        ("unauthenticated", None, status.HTTP_401_UNAUTHORIZED,
         status.HTTP_401_UNAUTHORIZED, None),
    ])
    def test_update_and_delete(self, user, detail_url, update_status_code, delete_status_code, expected_plate_no):
        """
        Test updating and deleting vehicle information.

        This test checks if different users can update and delete
        vehicle information according to their roles.
        """
        test_user = {
            "user": self.user,
            "user2": self.user2,
            "superuser": self.superuser,
            "unauthenticated": None
        }.get(user)

        if test_user:
            self.client.force_authenticate(user=test_user)
        else:
            self.client.logout()

        if detail_url is None:
            detail_url = self.detail_url(self.vehicle_info1.id)

        # Update test
        response = self.client.put(detail_url, self.data, format='json')
        assert response.status_code == update_status_code

        if update_status_code == status.HTTP_200_OK:
            Vehicle_info.objects.get(
                id=self.vehicle_info1.id).refresh_from_db()
            assert Vehicle_info.objects.get(
                id=self.vehicle_info1.id).plate_no == expected_plate_no

        # Delete test
        response = self.client.delete(detail_url)
        assert response.status_code == delete_status_code

        if delete_status_code == status.HTTP_204_NO_CONTENT:
            assert not Vehicle_info.objects.filter(
                id=self.vehicle_info1.id).exists()


@pytest.mark.django_db
class TestParkingDetailsView:
    @pytest.fixture(autouse=True)
    def set_up(self):
        """
        Setup method that runs before each test.

        Initializes the API client, creates test users, and sets up test data.
        """
        self.client = APIClient()
        self.url = reverse('parking-details')
        self.user = User.objects.create_user(
            username='user1', password='password123')
        self.user2 = User.objects.create_user(
            username='user2', password='password123')
        self.superuser = User.objects.create_superuser(
            username='admin', password='admin123')
        self.employee = User.objects.create_employee(
            username='employee', password='password123', is_staff=True)
        self.parking_space = ParkingSpace.objects.create(
            name="Parking Space", number=10, occupied=False, rate=123)
        self.parking_space2 = ParkingSpace.objects.create(
            name="Parking Space", number=1, occupied=False, rate=123)
        self.vehicle_info = Vehicle_info.objects.create(
            user=self.user, type="Car", plate_no="ABC123", parked=False)
        self.vehicle_info2 = Vehicle_info.objects.create(
            user=self.user2, type="Car", plate_no="ABC1234", parked=False)
        self.parking_details = ParkingDetails.objects.create(
            parking_space=self.parking_space, vehicle_info=self.vehicle_info, checkout_time="2024-11-11T11:11:00Z")
        self.parking_details2 = ParkingDetails.objects.create(
            parking_space=self.parking_space2, vehicle_info=self.vehicle_info2, checkout_time="2024-11-11T11:11:00Z")

    @pytest.mark.parametrize("user, expected_status_code, expected_count", [
        ("user", status.HTTP_200_OK, 1,),
        ("employee", status.HTTP_200_OK, 2,),
        ("superuser", status.HTTP_200_OK, 2, ),
    ])
    def test_list_parkingdetails(self, user, expected_status_code, expected_count):
        """
        Test listing parking details based on user roles.

        Verifies the number of parking details visible to different types of users.
        """
        self.client.force_authenticate(user=getattr(self, user))
        response = self.client.get(self.url)
        assert response.status_code == expected_status_code
        assert len(response.data['results']) == expected_count

    @pytest.mark.parametrize("user, expected_status_code, expected_count, expected_occupied, expected_parked, should_fail", [
        ("employee", status.HTTP_201_CREATED, 3, True, True, False),
        ("user", status.HTTP_403_FORBIDDEN, 2, False, False, True),
        ("employee", status.HTTP_400_BAD_REQUEST, 2, True, False, True),
    ])
    def test_create_parkingdetails(self, user, expected_status_code, expected_count, expected_occupied, expected_parked, should_fail):
        """
        Test creating parking details with different user roles and conditions.

        Checks if parking details can be created under various conditions and
          verifies the occupancy and parked status.
        """
        self.client.force_authenticate(user=getattr(self, user))

        if should_fail:
            self.parking_space.occupied = True
            self.parking_space.save()

        data = {"parking_space": self.parking_space.id,
                "vehicle_info": self.vehicle_info.id, "checkout_time": "2024-12-31T23:59:59Z"}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == expected_status_code
        assert ParkingDetails.objects.count() == expected_count

        if not should_fail:
            self.parking_space.refresh_from_db()
            assert self.parking_space.occupied == expected_occupied
            self.vehicle_info.refresh_from_db()
            assert self.vehicle_info.parked == expected_parked

    @pytest.mark.parametrize("user, parking_space_occupied, expected_status_code, expected_count, expected_error", [
        ("employee", True, status.HTTP_400_BAD_REQUEST,
         2, "parking spot is occupied"),
        ("employee", False, status.HTTP_201_CREATED, 3, ""),
    ])
    def test_create_parkingdetails_with_occupied_space(self, user, parking_space_occupied, expected_status_code, expected_count, expected_error):
        """
        Test creating parking details with an occupied parking space.

        Verifies that an attempt to create parking details with an already occupied parking space returns the correct error or success response.
        """
        self.client.force_authenticate(user=self.employee)
        self.parking_space.occupied = parking_space_occupied
        self.parking_space.save()

        data = {"parking_space": self.parking_space.id,
                "vehicle_info": self.vehicle_info.id, "checkout_time": "2024-12-31T23:59:59Z"}
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == expected_status_code
        assert ParkingDetails.objects.count() == expected_count
        if expected_error:
            assert expected_error in str(response.data)
