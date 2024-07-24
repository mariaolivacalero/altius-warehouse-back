import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import User


class TestViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user_data = {
            "username": "usertest",
            "email": "test@example.com",
            "password": "testpassword",
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_invalid_data(self):
        invalid_data = {"email": "", "password": ""}
        response = self.client.post(self.register_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_login_user(self):
        # Create a user
        user = User.objects.create_user(
            username="usertest", email="test@example.com", password="testpassword"
        )

        # Try to log in
        response = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_invalid_credentials(self):
        # Create a user
        user = User.objects.create_user(
            username="usertest", email="test@example.com", password="testpassword"
        )

        # Try to log in with invalid credentials
        invalid_data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_user_non_existent(self):
        # Try to log in with non-existent user
        response = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
