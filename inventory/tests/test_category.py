from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from inventory.models import Category
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class CategoryTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.category_data = {
            "name": "Test Category"
        }
        self.category = Category.objects.create(**self.category_data)

    def test_create_category(self):
        url = reverse('categories')
        new_category_data = {
            "name": "New Category"
        }
        response = self.client.post(url, new_category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        created_category = Category.objects.get(name=new_category_data['name'])
        self.assertEqual(created_category.name, new_category_data['name'])

    def test_get_category_list(self):
        url = reverse('categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('id', response.data[0])
        self.assertIn('name', response.data[0])

    def test_get_single_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.category.id)
        self.assertEqual(response.data['name'], self.category.name)

    def test_update_category(self):
        url = reverse('category-detail', args=[self.category.id])
        updated_data = {
            "name": "Updated Category"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.name, updated_data['name'])

    def test_delete_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

