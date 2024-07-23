from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item


class ItemAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item_data = {"name": "Test Item", "description": "Test Description"}
        self.response = self.client.post("/api/items/", self.item_data, format="json")

    def test_create_item(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, "Test Item")

    def test_get_items(self):
        response = self.client.get("/api/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_item(self):
        item = Item.objects.get()
        response = self.client.get(f"/api/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Item")

    def test_update_item(self):
        item = Item.objects.get()
        updated_data = {"name": "Updated Item", "description": "Updated Description"}
        response = self.client.put(
            f"/api/items/{item.id}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get().name, "Updated Item")

    def test_delete_item(self):
        item = Item.objects.get()
        response = self.client.delete(f"/api/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
