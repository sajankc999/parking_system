from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from REST_API.models import ParkingDetails, ParkingSpace, Vehicle_info
from REST_API.permissions import IsCustomer, IsEmployee, IsSuperUser

User = get_user_model()


class ParkingSpaceViewTests(APITestCase):
    def setUp(self):
        # self.url = reverse('api/parking_space')
        self.url = reverse("parkingspace-list")
        self.user = User.objects.create_user(
            username="user1", password="password123")
        self.employee = User.objects.create_user(
            username="employee", password="password123", employee=True, is_staff=True
        )
        self.superuser = User.objects.create_superuser(
            username="admin", password="admin123"
        )
        self.parking_space = ParkingSpace.objects.create(
            name="Parking Space 1", number=5, rate=200, occupied=False
        )

        self.detail_url = reverse(
            "parkingspace-detail", args=[self.parking_space.id])

    def test_create_parkingspace(self):
        # superuser test
        self.client.force_authenticate(user=self.superuser)

        data = {"name": "Parking Space 1",
                "number": 1, "rate": 20, "occupied": False}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingSpace.objects.count(), 2)
        self.assertEqual(
            ParkingSpace.objects.get(id=response.data["id"]).name, data["name"]
        )

        self.client.logout()

        # employee test
        self.client.force_authenticate(user=self.employee)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingSpace.objects.count(), 3)
        self.assertEqual(
            ParkingSpace.objects.get(id=response.data["id"]).name, data["name"]
        )

        # customer test
        self.client.logout()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_parkingspace(self):
        # superuser
        self.client.force_authenticate(user=self.superuser)
        data = {
            "name": "Updated Parking Space",
            "number": 6,
            "rate": 100,
            "occupied": False,
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parking_space.refresh_from_db()
        self.assertEqual(self.parking_space.name, data["name"])

        self.client.logout()
        # employee
        self.client.force_authenticate(user=self.employee)
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parking_space.refresh_from_db()
        self.assertEqual(self.parking_space.name, data["name"])

        self.client.logout()
        # customer
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_parking_space(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.delete(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.logout()
        # employee
        self.parking_space = ParkingSpace.objects.create(
            name="Parking Space 1", number=5, rate=200, occupied=False
        )
        self.detail_url = reverse(
            "parkingspace-detail", args=[self.parking_space.id])
        self.client.force_authenticate(user=self.employee)
        response = self.client.delete(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.logout()
        # customer
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class VehicleInfoViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("vehicleinfo-list")
        self.user = User.objects.create_user(
            username="user1", password="password123")
        self.user2 = User.objects.create_user(
            username="user2", password="password123")
        self.superuser = User.objects.create_superuser(
            username="admin", password="admin123"
        )
        self.owner = User.objects.get(username='user1')
        self.vehicle_info1 = Vehicle_info.objects.create(
            user=self.user, type='car', plate_no='123')
        self.vehicle_info2 = Vehicle_info.objects.create(
            user=self.user2, type='bike', plate_no='333')
        self.detail_url = reverse(
            "vehicleinfo-detail", args=[self.vehicle_info1.id])
        self.detail_url2 = reverse(
            "vehicleinfo-detail", args=[self.vehicle_info2.id])

        self.data = {

            "type": "bus",
            "plate_no": "444",

        }

    def test_retrieve_vehicleinfo(self):
        # without login user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # with login user
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # owner getting own data:
        self.client.logout()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        # print("RESPONE::::",response.data)
        self.assertEqual(len(response.data['results']), 1)

        # admin user and staff can retrieve all results

        self.client.logout()
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_vehicleinfo(self):

        # only user can create vehicle_info
        self.client.force_authenticate(user=self.user)
        # print("OWNER::::",self.owner)

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle_info.objects.filter(
            user=self.user).count(), 2)

        # None user create
        self.client.logout()
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # vehicel already exists
        self.client.logout()

        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("vehicle already exists", str(response.data))

    def test_update_and_delete(self):
        # only rightful owner can update and delete his/her data
        self.client.force_authenticate(user=self.user)
        # can update and delete his data
        response = self.client.put(self.detail_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vehicle_info1.refresh_from_db()
        self.assertEqual(self.vehicle_info1.plate_no, self.data["plate_no"])
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # cant delete/update others

        response = self.client.put(self.detail_url2, self.data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(self.detail_url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.logout()
        # admin users can delete and update all
        self.client.force_authenticate(user=self.superuser)
        # can update and delete his data
        Vehicle_info.objects.create(
            user=self.user2, type='bike', plate_no='333')
        response = self.client.put(self.detail_url2, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vehicle_info2.refresh_from_db()
        self.assertEqual(self.vehicle_info2.plate_no, self.data["plate_no"])
        response = self.client.delete(self.detail_url2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ParkingDetailsViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('parking-details')
        self.user = User.objects.create_user(
            username='user1', password='password123', customer=True)
        self.user2 = User.objects.create_user(
            username='user2', password='password123', customer=True)

        self.superuser = User.objects.create_superuser(
            username='admin', password='admin123')

        self.employee = User.objects.create_employee(
            username='employee', password='password123')

        self.parking_space = ParkingSpace.objects.create(
            name="Parking Space", number=10, occupied=False, rate=123)
        self.parking_space2 = ParkingSpace.objects.create(
            name="Parking Space", number=1, occupied=False, rate=123)

        self.vehicle_info = Vehicle_info.objects.create(
            user=self.user, type="Car", plate_no="ABC123", parked=False)
        self.vehicle_info2 = Vehicle_info.objects.create(
            user=self.user2, type="Car", plate_no="ABC1234", parked=False)
        self.parking_details = ParkingDetails.objects.create(
            parking_space=self.parking_space,
            vehicle_info=self.vehicle_info,
            checkout_time="2024-11-11T11:11:00Z"
        )
        self.parking_details = ParkingDetails.objects.create(
            parking_space=self.parking_space2,
            vehicle_info=self.vehicle_info2,
            checkout_time="2024-11-11T11:11:00Z"
        )

    def test_list_parkingdetails_as_customer(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), ParkingDetails.objects.filter(
            vehicle_info__user=self.user).count())

    def test_list_parkingdetails_as_admin_or_emp(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']), ParkingDetails.objects.count())
        self.client.logout()
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']), ParkingDetails.objects.count())

    def test_create_parkingdetails(self):
        self.client.force_authenticate(user=self.employee)
        data = {
            "parking_space": self.parking_space.id,
            "vehicle_info": self.vehicle_info.id,
            "checkout_time": "2024-12-31T23:59:59Z"
        }
        response = self.client.post(self.url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingDetails.objects.count(), 3)
        self.parking_space.refresh_from_db()
        self.assertTrue(self.parking_space.occupied)
        self.vehicle_info.refresh_from_db()
        self.assertTrue(self.vehicle_info.parked)

    def test_create_parkingdetails_asCustomer(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "parking_space": self.parking_space.id,
            "vehicle_info": self.vehicle_info.id,
            "checkout_time": "2024-12-31T23:59:59Z"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ParkingDetails.objects.count(), 2)
        # self.parking_space.refresh_from_db()
        self.assertTrue(not self.parking_space.occupied)
        self.vehicle_info.refresh_from_db()
        self.assertTrue(not self.vehicle_info.parked)

    def test_create_parkingdetails_with_occupied_space(self):
        self.client.force_authenticate(user=self.employee)
        self.parking_space.occupied = True
        self.parking_space.save()
        data = {
            "parking_space": self.parking_space.id,
            "vehicle_info": self.vehicle_info.id,
            "checkout_time": "2024-12-31T23:59:59Z"
        }
        response = self.client.post(self.url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("parking spot is occupied", str(response.data))
