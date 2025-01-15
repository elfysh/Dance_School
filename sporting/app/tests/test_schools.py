import json
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APIClient
from app import models

class SchoolsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dance_school = models.DanceSchool.objects.create(
            dance_school_name='Test School',
            dance_school_address='123 Test St',
            phone_number='+7 123 456 78 90'
        )
        self.admin_user = models.AdminUser.objects.create(username='admin', password='password')
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post(reverse('api_admin_login'), urlencode({'username': 'admin', 'password': 'password'}), content_type='application/x-www-form-urlencoded')
        return response.headers['Token']

    def test_create_school(self):
        data = {
            'name': 'New School',
            'address': '456 New St',
            'phone': '+7 987 654 32 10'
        }
        response = self.client.post(reverse('api_add_school'), urlencode(data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.DanceSchool.objects.count(), 2)
        self.assertEqual(models.DanceSchool.objects.last().dance_school_name, 'New School')

    def test_edit_school(self):
        new_data = {
            'name': 'Updated School',
            'address': '789 Updated St',
            'phone': '+7 123 456 78 90'
        }
        response = self.client.post(reverse('api_edit_school', args=[self.dance_school.dance_school_id]), urlencode(new_data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dance_school.refresh_from_db()
        self.assertEqual(self.dance_school.dance_school_name, 'Updated School')

    def test_delete_school(self):
        response = self.client.delete(reverse('api_delete_school', args=[self.dance_school.dance_school_id]), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.DanceSchool.objects.count(), 0)

    def test_get_schools(self):
        response = self.client.get(reverse('api_get_schools'), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['schools']), 1)
        self.assertEqual(response.json()['schools'][0]['name'], 'Test School')