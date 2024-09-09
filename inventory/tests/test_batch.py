from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from inventory.models import Batch, Party
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class BatchTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user_data = {"username": "testuser", "password": "testpassword123"}
        self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Corrected to use the correct variable name: self.party_data
        self.party_data = {"name": "Test Party"}
        self.party = Party.objects.create(**self.party_data)

        self.batch_data = {
            "receiving_date": "2023-08-01",
            "party": self.party,  # Use the Party instance, not the ID here
            "total_quantity": 100,
            "notes": "Initial batch",
            "receiptID": "RB123456",
            "type": "reception"
        }
        self.batch = Batch.objects.create(**self.batch_data)

    def test_create_batch(self):
        url = reverse("batches")
        new_batch_data = {
            "receiving_date": "2023-08-02",
            "party": self.party.id,  # Use the party ID in the API request
            "total_quantity": 200,
            "notes": "Second batch",
            "receiptID": "RB123457",
            "type": "reception"
        }
        response = self.client.post(url, new_batch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Batch.objects.count(), 2)
        created_batch = Batch.objects.get(receiptID=new_batch_data["receiptID"])
        self.assertEqual(created_batch.receiptID, new_batch_data["receiptID"])

    def test_create_batch_bad_request(self):
        url = reverse("batches")
        new_batch_data = {}
        response = self.client.post(url, new_batch_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_get_batch_list(self):
        url = reverse("batches")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("id", response.data[0])
        self.assertIn("receiptID", response.data[0])

    def test_get_single_batch(self):
        url = reverse("batch-detail", args=[self.batch.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.batch.id)
        self.assertEqual(response.data["receiptID"], self.batch.receiptID)

    def test_get_single_batch_not_found(self):
        url = reverse("batch-detail", args=["1234"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_batch(self):
        url = reverse("batch-detail", args=[self.batch.id])
        updated_data = {
            "receiving_date": "2023-08-03",
            "party": self.party.id,  # Use the ID in the API request
            "total_quantity": 150,
            "notes": "Updated batch",
            "receiptID": "RB123456",
            "type": "reception"
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_batch = Batch.objects.get(id=self.batch.id)  # Corrected self.batch.id
        self.assertEqual(updated_batch.total_quantity, updated_data["total_quantity"])
        self.assertEqual(updated_batch.notes, updated_data["notes"])

    def test_update_batch_bad_request(self):
        url = reverse("batch-detail", args=[self.batch.id])
        updated_data = {}
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_delete_batch(self):
        url = reverse("batch-detail", args=[self.batch.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Batch.objects.count(), 0)
