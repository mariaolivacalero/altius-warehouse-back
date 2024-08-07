from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from inventory.models import Product
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class InventoryViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Create a product to use in tests
        self.product_data = {
            "name": "Test Product",
            "ean": "8123456654321",
            "description": "description",
            "category": "category",
            "unit_of_measure": "kilogram"
        }
        self.product = Product.objects.create(**self.product_data)

    def test_create_product(self):
        url = reverse('products')
        new_product_data = {
            "name": "New Product",
            "ean": "8123456654322",
            "description": "New description",
            "category": "New category",
            "unit_of_measure": "liter"
        }
        response = self.client.post(url, new_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        created_product = Product.objects.get(name=new_product_data['name'])
        self.assertEqual(created_product.name, new_product_data['name'])

    def test_get_product_list(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('id', response.data[0])
        self.assertIn('name', response.data[0])

    def test_get_single_product(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product.id)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product(self):
        url = reverse('product-detail', args=[self.product.id])
        updated_data = {
            "name": "Updated Product",
            "ean": "8123456654321",
            "description": "updated description",
            "category": "updated category",
            "unit_of_measure": "kilogram"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, updated_data['name'])

    def test_delete_product(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
