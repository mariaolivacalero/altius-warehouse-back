# custom_auth/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group


User = get_user_model()

class UserGroupTests(APITestCase):

    def setUp(self):
        # Create groups
        self.beneficiaries_group = Group.objects.create(name='Beneficiaries')
        self.food_bank_staff_group = Group.objects.create(name='Food Bank Staff')
        self.volunteers_group = Group.objects.create(name='Volunteers')
        self.system_administrators_group = Group.objects.create(name='System Administrators')

        # Create users
        self.user_beneficiary = User.objects.create_user(
            email='beneficiary@example.com',
            username='beneficiary',
            password='password123'
        )
        self.user_food_bank_staff = User.objects.create_user(
            email='foodbankstaff@example.com',
            username='foodbankstaff',
            password='password123'
        )
        self.user_volunteer = User.objects.create_user(
            email='volunteer@example.com',
            username='volunteer',
            password='password123'
        )
        self.user_system_administrator = User.objects.create_user(
            email='sysadmin@example.com',
            username='sysadmin',
            password='password123'
        )

        # Assign groups to users
       
        self.user_food_bank_staff.groups.add(self.food_bank_staff_group)
        self.user_volunteer.groups.add(self.volunteers_group)
        self.user_system_administrator.groups.add(self.system_administrators_group)

        # Since users are created with beneficiaries as default group, we need to remove that group from the users
        
        self.user_food_bank_staff.groups.remove(self.beneficiaries_group)
        self.user_volunteer.groups.remove(self.beneficiaries_group)
        self.user_system_administrator.groups.remove(self.beneficiaries_group)

   
    
    def test_is_beneficiary(self):
        self.assertTrue(self.user_beneficiary.is_beneficiary())
        self.assertFalse(self.user_food_bank_staff.is_beneficiary())
        self.assertFalse(self.user_volunteer.is_beneficiary())
        self.assertFalse(self.user_system_administrator.is_beneficiary())

    def test_is_food_bank_staff(self):
        self.assertTrue(self.user_food_bank_staff.is_food_bank_staff())
        self.assertFalse(self.user_beneficiary.is_food_bank_staff())
        self.assertFalse(self.user_volunteer.is_food_bank_staff())
        self.assertFalse(self.user_system_administrator.is_food_bank_staff())

    def test_is_volunteer(self):
        self.assertTrue(self.user_volunteer.is_volunteer())
        self.assertFalse(self.user_beneficiary.is_volunteer())
        self.assertFalse(self.user_food_bank_staff.is_volunteer())
        self.assertFalse(self.user_system_administrator.is_volunteer())

    def test_is_system_administrator(self):
        self.assertTrue(self.user_system_administrator.is_system_administrator())
        self.assertFalse(self.user_beneficiary.is_system_administrator())
        self.assertFalse(self.user_food_bank_staff.is_system_administrator())
        self.assertFalse(self.user_volunteer.is_system_administrator())

    