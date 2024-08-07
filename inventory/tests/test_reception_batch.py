# inventory/tests/test_reception_batch.py

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from inventory.models import ReceptionBatch, Supplier
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class ReceptionBatchTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.supplier_data = {
            "name": "Test Supplier"
        }
        self.supplier = Supplier.objects.create(**self.supplier_data)
        
        self.reception_batch_data = {
            "receiving_date": "2023-08-01",
            "supplier": self.supplier,
            "total_quantity": 100,
            "notes": "Initial batch",
            "receiptID": "RB123456"
        }
        self.reception_batch = ReceptionBatch.objects.create(**self.reception_batch_data)

    def test_create_reception_batch(self):
        url = reverse('reception-batches')
        new_reception_batch_data = {
            "receiving_date": "2023-08-02",
            "supplier": self.supplier.id,
            "total_quantity": 200,
            "notes": "Second batch",
            "receiptID": "RB123457"
        }
        response = self.client.post(url, new_reception_batch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReceptionBatch.objects.count(), 2)
        created_reception_batch = ReceptionBatch.objects.get(receiptID=new_reception_batch_data['receiptID'])
        self.assertEqual(created_reception_batch.receiptID, new_reception_batch_data['receiptID'])

    def test_get_reception_batch_list(self):
        url = reverse('reception-batches')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('id', response.data[0])
        self.assertIn('receiptID', response.data[0])

    def test_get_single_reception_batch(self):
        url = reverse('reception-batch-detail', args=[self.reception_batch.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.reception_batch.id)
        self.assertEqual(response.data['receiptID'], self.reception_batch.receiptID)

    def test_update_reception_batch(self):
        url = reverse('reception-batch-detail', args=[self.reception_batch.id])
        updated_data = {
            "receiving_date": "2023-08-03",
            "supplier": self.supplier.id,
            "total_quantity": 150,
            "notes": "Updated batch",
            "receiptID": "RB123456"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_reception_batch = ReceptionBatch.objects.get(id=self.reception_batch.id)
        self.assertEqual(updated_reception_batch.total_quantity, updated_data['total_quantity'])
        self.assertEqual(updated_reception_batch.notes, updated_data['notes'])

    def test_delete_reception_batch(self):
        url = reverse('reception-batch-detail', args=[self.reception_batch.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ReceptionBatch.objects.count(), 0)
