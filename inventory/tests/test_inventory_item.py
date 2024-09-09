from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from inventory.models import (
    AdministrativeUnit,
    InventoryItem,
    Location,
    Product,
    Category,
    Party,
    Batch,
    Reception,
    Dispatch,
    StoreStocking,
)
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from django.core.exceptions import ValidationError

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

        self.administrative_unit = AdministrativeUnit.objects.create(name="Unit 1")
        self.location_data = {"administrative_unit": self.administrative_unit, "type": "warehouse"}
        self.location = Location.objects.create(**self.location_data)

        self.product_data = {
            "name": "Test Product",
            "code": "8123456654321",
            "description": "description",
            "category": self.category,
            "unit_of_measure": "kilogram",
            "manufacturer": "Test manufacturer"
        }
        self.product = Product.objects.create(**self.product_data)
        
        self.today_date = now().date()
        self.party_data = {"name": "Test Supplier", "type": "supplier"}
        self.party = Party.objects.create(**self.party_data)
        
        self.batch_data = {
            "receiving_date": self.today_date,
            "party": self.party,
            "total_quantity": 100,
            "notes": "Initial batch",
            "receiptID": "RB123456",
            "type": "reception",
        }
        self.batch = Batch.objects.create(**self.batch_data)

        self.inventory_item_data = {
            "product": self.product,
            "batch": self.batch,
            "quantity": 50,
            "warehouse_quantity": 40,
            "storefront_quantity": 10,
            "administrative_unit": self.administrative_unit,
            "expiration_date": self.today_date,
        }
        self.inventory_item = InventoryItem.objects.create(**self.inventory_item_data)

    def test_create_inventory_item(self):
        url = reverse("inventory-items")
        new_batch = Batch.objects.create(
            receiving_date=self.today_date,
            party=self.party,
            total_quantity=50,
            notes="New batch",
            receiptID="RB789012",
            type="reception",
        )
        new_inventory_item_data = {
            "product": self.product.id,
            "batch": new_batch.id,
            "quantity": 30,
            "warehouse_quantity": 25,
            "storefront_quantity": 5,
            "administrative_unit": self.administrative_unit.id,
            "expiration_date": self.today_date,
        }
        response = self.client.post(url, new_inventory_item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 2)
        created_inventory_item = InventoryItem.objects.get(
            product_id=new_inventory_item_data["product"],
            batch_id=new_inventory_item_data["batch"]
        )
        self.assertEqual(created_inventory_item.quantity, new_inventory_item_data["quantity"])
        self.assertEqual(Reception.objects.count(), 2)  # One for setUp, one for new item

    def test_add_stock(self):
        initial_quantity = self.inventory_item.quantity
        initial_warehouse_quantity = self.inventory_item.warehouse_quantity
        initial_reception_count = Reception.objects.count()
        self.inventory_item.add_stock(10, user=self.user)
        self.inventory_item.refresh_from_db()
        self.assertEqual(self.inventory_item.quantity, initial_quantity + 10)
        self.assertEqual(self.inventory_item.warehouse_quantity, initial_warehouse_quantity + 10)
        self.assertEqual(Reception.objects.count(), initial_reception_count + 1)

    def test_remove_stock(self):
        initial_quantity = self.inventory_item.quantity
        initial_warehouse_quantity = self.inventory_item.warehouse_quantity
        self.inventory_item.remove_stock(10, user=self.user)
        self.inventory_item.refresh_from_db()
        self.assertEqual(self.inventory_item.quantity, initial_quantity - 10)
        self.assertEqual(self.inventory_item.warehouse_quantity, initial_warehouse_quantity - 10)
        self.assertEqual(Dispatch.objects.count(), 1)

    def test_remove_stock_validation_error(self):
        with self.assertRaises(ValidationError):
            self.inventory_item.remove_stock(self.inventory_item.quantity + 1, user=self.user)

    def test_transfer_stock(self):
        target_administrative_unit = AdministrativeUnit.objects.create(name="Unit 2")
        target_location = Location.objects.create(administrative_unit=target_administrative_unit, type="warehouse")
        target_inventory_item = InventoryItem.objects.create(
            product=self.product,
            batch=self.batch,
            quantity=0,
            warehouse_quantity=0,
            storefront_quantity=0,
            administrative_unit=target_administrative_unit,
            expiration_date=self.today_date,
        )
        initial_quantity = self.inventory_item.quantity
        initial_reception_count = Reception.objects.count()
        transfer_quantity = 10
        self.inventory_item.transfer_stock(transfer_quantity, target_inventory_item, user=self.user)
        
        self.inventory_item.refresh_from_db()
        target_inventory_item.refresh_from_db()
        
        self.assertEqual(self.inventory_item.quantity, initial_quantity - transfer_quantity)
        self.assertEqual(target_inventory_item.quantity, transfer_quantity)
        self.assertEqual(Dispatch.objects.count(), 1)
        self.assertEqual(Reception.objects.count(), initial_reception_count + 1)
        self.assertEqual(StoreStocking.objects.count(), 1)

    def test_get_inventory_item_list(self):
        url = reverse("inventory-items")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("id", response.data[0])
        self.assertIn("product", response.data[0])
        self.assertIn("quantity", response.data[0])
        self.assertIn("administrative_unit", response.data[0])

    def test_get_single_inventory_item(self):
        url = reverse("inventory-items-detail", args=[self.inventory_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.inventory_item.id)
        self.assertEqual(response.data["administrative_unit"], self.inventory_item.administrative_unit.id)

    def test_get_single_inventory_item_not_found(self):
        url = reverse("inventory-items-detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_inventory_item(self):
        url = reverse("inventory-items-detail", args=[self.inventory_item.id])
        new_administrative_unit = AdministrativeUnit.objects.create(name="Unit 2")
        updated_data = {
            "product": self.product.id,
            "batch": self.batch.id,
            "quantity": 60,
            "warehouse_quantity": 50,
            "storefront_quantity": 10,
            "administrative_unit": new_administrative_unit.id,
            "expiration_date": self.today_date,
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_inventory_item = InventoryItem.objects.get(id=self.inventory_item.id)
        self.assertEqual(updated_inventory_item.quantity, updated_data["quantity"])
        self.assertEqual(updated_inventory_item.administrative_unit.id, updated_data["administrative_unit"])

    def test_update_inventory_item_bad_request(self):
        url = reverse("inventory-items-detail", args=[self.inventory_item.id])
        updated_data = {}
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_inventory_item(self):
        url = reverse("inventory-items-detail", args=[self.inventory_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InventoryItem.objects.count(), 0)