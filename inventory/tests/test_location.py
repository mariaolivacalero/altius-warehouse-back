from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from inventory.models import Location, AdministrativeUnit
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class LocationTest(TestCase):

    """ def setUp(self):
        self.client = APIClient()

        self.user_data = {"username": "testuser", "password": "testpassword123"}
        self.user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # Set up required data for AdministrativeUnit
        self.administrative_unit = AdministrativeUnit.objects.create(name="Unit 1")

        # Updated location_data to include administrative_unit and type
        self.location_data = {
            "administrative_unit": self.administrative_unit,
            "type": "warehouse"
        }
        self.location = Location.objects.create(**self.location_data)

    def test_create_location(self):
        url = reverse("locations")
        new_location_data = {
            "administrative_unit": self.administrative_unit.id,  # Use id for ForeignKey field
            "type": "storefront",  # Use one of the valid choices
        }
        response = self.client.post(url, new_location_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)
        created_location = Location.objects.get(id=response.data["id"])
        self.assertEqual(created_location.type, new_location_data["type"])
        self.assertEqual(created_location.administrative_unit.id, new_location_data["administrative_unit"])

    def test_create_location_bad_request(self):
        url = reverse("locations")
        # Missing required fields for `administrative_unit` and `type`
        new_location_data = {}
        response = self.client.post(url, new_location_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_location_list(self):
        url = reverse("locations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("id", response.data[0])
        self.assertIn("administrative_unit", response.data[0])  # Verify presence of new field
        self.assertIn("type", response.data[0])  # Verify presence of new field

    def test_get_single_location(self):
        url = reverse("location-detail", args=[self.location.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.location.id)
        self.assertEqual(response.data["administrative_unit"], self.location.administrative_unit.id)
        self.assertEqual(response.data["type"], self.location.type)

    def test_get_single_location_not_found(self):
        url = reverse("location-detail", args=["1234"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_location(self):
        url = reverse("location-detail", args=[self.location.id])
        updated_data = {
            "administrative_unit": self.administrative_unit.id,  # Keeping the same administrative unit
            "type": "storefront"  # Updating the type field
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_location = Location.objects.get(id=self.location.id)
        self.assertEqual(updated_location.type, updated_data["type"])

    def test_update_location_bad_request(self):
        url = reverse("location-detail", args=[self.location.id])
        updated_data = {}  # Missing required fields
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_location(self):
        url = reverse("location-detail", args=[self.location.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Location.objects.count(), 0) """

