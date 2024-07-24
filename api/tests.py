from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

from custom_auth.models import User
from .models import Item
from rest_framework_simplejwt.tokens import RefreshToken


class ItemAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
           username="usertest",  email="test@example.com", password="testpassword"
        )
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = self.refresh_token.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.item_data = {"name": "Test Item", "description": "Test Description"}

    def test_create_item(self):
        response = self.client.post("/api/items/", self.item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, "Test Item")

    def test_get_items(self):
        response = self.client.get("/api/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Since there are no items created in the setup, count should be 0
        self.assertEqual(len(response.data), 0)

        # Create an item and try again
        self.client.post("/api/items/", self.item_data, format="json")
        response = self.client.get("/api/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_item(self):
        item = Item.objects.create(name="Test Item", description="Test Description")
        response = self.client.get(f"/api/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Item")

    def test_update_item(self):
        item = Item.objects.create(name="Test Item", description="Test Description")
        updated_data = {"name": "Updated Item", "description": "Updated Description"}
        response = self.client.put(
            f"/api/items/{item.id}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get().name, "Updated Item")

    def test_delete_item(self):
        item = Item.objects.create(name="Test Item", description="Test Description")
        response = self.client.delete(f"/api/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_unauthenticated(self):
        # Clear the credentials to simulate an unauthenticated request
        self.client.credentials()
        response = self.client.post("/api/items/", self.item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Item.objects.count(), 0)
