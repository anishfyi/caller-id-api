from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Contact, SpamReport
from django.urls import reverse
from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
import json
import csv
from io import StringIO
from rest_framework_simplejwt.tokens import RefreshToken
import pytest

User = get_user_model()

@override_settings(REST_FRAMEWORK={
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {}
})
class PhoneNumberValidationTest(APITestCase):
    """
    Test cases for phone number validation in contacts and spam reports.
    """
    def setUp(self):
        """Create a test user and authenticate"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Anish'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

@override_settings(REST_FRAMEWORK={
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {}
})
class SpamTest(APITestCase):
    def setUp(self):
        """Create a user and authenticate"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Anish'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_check_spam(self):
        """Test checking spam likelihood"""
        # Create some spam reports and contacts
        SpamReport.objects.create(
            reporter=self.user,
            phone_number='+12125551234'
        )
        Contact.objects.create(
            owner=self.user,
            name='John Doe',
            phone_number='+12125551234'
        )
        
        response = self.client.get('/api/spam/check/+12125551234/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['spam_likelihood'], 50.0)

@override_settings(DEBUG=True, REST_FRAMEWORK={
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {}
})
class BulkOperationsTest(APITestCase):
    def setUp(self):
        """Create a user and authenticate"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Anish'
        )
        # Get token
        refresh = RefreshToken.for_user(self.user)
        
        # Setup client with token auth
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Create a sample contact
        self.contact = Contact.objects.create(
            owner=self.user,
            name='Existing Contact',
            phone_number='+12125551234'
        )
        
    @override_settings(DEBUG=True, REST_FRAMEWORK={
        'DEFAULT_THROTTLE_CLASSES': [],
        'DEFAULT_THROTTLE_RATES': {}
    })
    class ExportJSONTest(APITestCase):
        def setUp(self):
            """Create a user and authenticate"""
            self.user = User.objects.create_user(
                username='testuser',
                password='testpass123',
                first_name='Anish'
            )
            # Get token
            refresh = RefreshToken.for_user(self.user)
            
            # Setup client with token auth
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
            
            # Create a sample contact
            self.contact = Contact.objects.create(
                owner=self.user,
                name='Existing Contact',
                phone_number='+12125551234'
            )

        def test_contact_export_json(self):
            """Test exporting contacts as JSON"""
            # Try alternative URLs
            urls_to_try = [
                '/api/contacts/export/',
                '/api/export-contacts/',
                '/api/export/'
            ]
            
            for url in urls_to_try:
                response = self.client.get(url, {'format': 'json'})
                print(f"Export JSON response: {response.status_code}, URL: {url}")
                
                if response.status_code == status.HTTP_200_OK:
                    print(f"Success with URL: {url}")
                    
                    self.assertTrue('application/json' in response['Content-Type'])
                    
                    # Verify content
                    content = json.loads(response.content.decode('utf-8'))
                    self.assertEqual(len(content), 1)
                    self.assertEqual(content[0]['name'], 'Existing Contact')
                    return
            
            # If we get here, none of the URLs worked
            self.fail("None of the export URLs worked")
