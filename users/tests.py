from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserProfile
import pytest

# Create your tests here.

class UserRegistrationTest(APITestCase):
    def test_user_registration_success(self):
        """Test that a user can register with valid data"""
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'phone_number': '+12125551234',
            'name': 'Test User'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertEqual(User.objects.get(username='testuser').get_full_name(), 'Test User')

    def test_user_registration_duplicate_phone(self):
        """Test that registration fails with duplicate phone number"""
        # Create first user
        User.objects.create_user(username='user1', password='pass123')
        UserProfile.objects.filter(user__username='user1').update(phone_number='+12125551234')

        # Try to create second user with same phone
        data = {
            'username': 'user2',
            'password': 'pass123',
            'phone_number': '+12125551234',
            'name': 'User Two'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserAuthenticationTest(APITestCase):
    def setUp(self):
        """Create a user for authentication tests"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Anish'
        )
        UserProfile.objects.filter(user=self.user).update(phone_number='+1234567890')

    def test_user_login_success(self):
        """Test that a user can login with valid credentials"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """Test that login fails with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post('/api/auth/token/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
