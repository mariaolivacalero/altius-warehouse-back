
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from inventory.models import Location
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class LocationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.location_data = {
            "name": "Test Location"
        }
        self.location = Location.objects.create(**self.location_data)

    def test_create_location(self):
        url = reverse('locations')
        new_location_data = {
            "name": "New Location"
        }
        response = self.client.post(url, new_location_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)
        created_location = Location.objects.get(name=new_location_data['name'])
        self.assertEqual(created_location.name, new_location_data['name'])

    def test_get_location_list(self):
        url = reverse('locations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('id', response.data[0])
        self.assertIn('name', response.data[0])

    def test_get_single_location(self):
        url = reverse('location-detail', args=[self.location.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.location.id)
        self.assertEqual(response.data['name'], self.location.name)

    def test_update_location(self):
        url = reverse('location-detail', args=[self.location.id])
        updated_data = {
            "name": "Updated Location"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_location = Location.objects.get(id=self.location.id)
        self.assertEqual(updated_location.name, updated_data['name'])

    def test_delete_location(self):
        url = reverse('location-detail', args=[self.location.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Location.objects.count(), 0)

