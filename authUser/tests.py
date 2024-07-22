# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserTest(APITestCase):
    """Test model for user Model"""

    def setUp(self):
        self.url = reverse("user")

    def test_create_user_success(self):
        data = {
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, data["username"])
