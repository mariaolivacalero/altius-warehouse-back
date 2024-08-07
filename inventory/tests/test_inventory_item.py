from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from inventory.models import (
    InventoryItem,
    Location,
    Product,
    Category,
    Supplier,
    ReceptionBatch,
)
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

User = get_user_model()


class InventoryItemTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user_data = {"username": "testuser", "password": "testpassword123"}
        self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.category_data = {"name": "Test Category"}
        self.category = Category.objects.create(**self.category_data)

        self.location_data = {"name": "Test Location"}
        self.location = Location.objects.create(**self.location_data)

        self.product_data = {
            "name": "Test Product",
            "ean": "8123456654321",
            "description": "description",
            "category": self.category,
            "unit_of_measure": "kilogram",
        }
        self.product = Product.objects.create(**self.product_data)
        self.today_date = datetime.today().date()  # Ensure this is a date object
        self.supplier_data = {"name": "Test Supplier"}
        self.supplier = Supplier.objects.create(**self.supplier_data)
        self.reception_batch_data = {
            "receiving_date": self.today_date,
            "supplier": self.supplier,
            "total_quantity": 100,
            "notes": "Initial batch",
            "receiptID": "RB123456",
        }
        self.reception_batch = ReceptionBatch.objects.create(
            **self.reception_batch_data
        )

        self.inventory_item_data = {
            "product": self.product,
            "reception_batch": self.reception_batch,
            "quantity": 1,
            "location": self.location,
            "expiration_date": self.today_date,
            "lot_number": 1,
        }
        self.inventory_item = InventoryItem.objects.create(**self.inventory_item_data)

    def test_create_inventory_item(self):
        url = reverse("inventory-items")
        new_inventory_item_data = {
            "product": self.product.id,
            "reception_batch": self.reception_batch.id,
            "quantity": 15,
            "location": self.location.id,
            "expiration_date": self.today_date,
            "lot_number": 2,
        }
        response = self.client.post(url, new_inventory_item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 2)
        created_inventory_item = InventoryItem.objects.get(
            lot_number=new_inventory_item_data["lot_number"]
        )
        self.assertEqual(
            created_inventory_item.location.id, new_inventory_item_data["location"]
        )

    def test_get_inventory_item_list(self):
        url = reverse("inventory-items")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("id", response.data[0])
        self.assertIn("product", response.data[0])
        self.assertIn("quantity", response.data[0])
        self.assertIn("location", response.data[0])

    def test_get_single_inventory_item(self):
        url = reverse("inventory-items-detail", args=[self.inventory_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.inventory_item.id)
        self.assertEqual(
            response.data["location"], self.inventory_item.location.id
        )

    def test_update_inventory_item(self):
        url = reverse("inventory-items-detail", args=[self.inventory_item.id])
        location_data = {"name": "Test Location"}
        new_location = Location.objects.create(**location_data)
        updated_data = {
            "product": self.product.id,
            "reception_batch": self.reception_batch.id,
            "quantity": 20,
            "location": new_location.id,
            "expiration_date": self.today_date,
            "lot_number": 3,
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_inventory_item = InventoryItem.objects.get(id=self.inventory_item.id)
        self.assertEqual(updated_inventory_item.quantity, updated_data["quantity"])
        self.assertEqual(updated_inventory_item.location.id, updated_data["location"])

    def test_delete_inventory_item(self):
        url = reverse("inventory-items-detail", args=[self.inventory_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InventoryItem.objects.count(), 0)
