# Create your tests here.
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUser:
    """
    Test suite for the User model API.

    This class contains tests to ensure that the User model API
    behaves as expected.
    """

    @pytest.fixture(autouse=True)
    def set_up(self):
        """
        Setup method that runs before each test.

        This method initializes the API client and sets the URL for
        the user endpoint.
        """
        self.client = APIClient()
        self.url = reverse("user")

    def test_create_user_success(self):
        """
        Test that a user can be created successfully.

        This test sends a POST request to the user creation endpoint
        and verifies that the user is created with the correct details.
        """
        data = {
            "username": "testuser",
            "password": "password123",
            "email": "test@example.com",
        }
        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED, "Expected status code to be 201 CREATED"
        assert User.objects.count() == 1, "Expected exactly one user to be created"
        assert User.objects.get(
        ).username == data["username"], "Expected the created user's username to match the input data"
