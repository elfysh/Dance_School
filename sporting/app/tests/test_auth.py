import json
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APIClient
from app import models

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = models.AdminUser.objects.create(username='admin', password='password')

    def test_admin_login(self):
        self.assertIsNotNone(models.AdminUser.objects.filter(username='admin').first())

        response = self.client.post(reverse('api_admin_login'), urlencode({'username': 'admin', 'password': 'password'}), content_type='application/x-www-form-urlencoded')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Token', response.headers)
        self.token = response.headers['Token']