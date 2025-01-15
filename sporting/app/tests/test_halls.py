import json
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APIClient
from app import models

class HallsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dance_school = models.DanceSchool.objects.create(
            dance_school_name='Test School',
            dance_school_address='123 Test St',
            phone_number='+7 123 456 78 90'
        )
        self.hall = models.Hall.objects.create(
            hall_name='Test Hall',
            capacity=100,
            dance_school_id=self.dance_school
        )
        self.admin_user = models.AdminUser.objects.create(username='admin', password='password')
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post(reverse('api_admin_login'), urlencode({'username': 'admin', 'password': 'password'}), content_type='application/x-www-form-urlencoded')
        return response.headers['Token']

    def test_create_hall(self):
        data = {
            'name': 'New Hall',
            'capacity': 150,
            'dance_school': self.dance_school.dance_school_id
        }
        response = self.client.post(reverse('api_add_hall'), urlencode(data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Hall.objects.count(), 2)
        self.assertEqual(models.Hall.objects.last().hall_name, 'New Hall')

    def test_edit_hall(self):
        new_data = {
            'name': 'Updated Hall',
            'capacity': 200,
            'dance_school': self.dance_school.dance_school_id
        }
        response = self.client.post(reverse('api_edit_hall', args=[self.hall.hall_id]), urlencode(new_data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hall.refresh_from_db()
        self.assertEqual(self.hall.hall_name, 'Updated Hall')

    def test_delete_hall(self):
        response = self.client.delete(reverse('api_delete_hall', args=[self.hall.hall_id]), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Hall.objects.count(), 0)

    def test_get_halls(self):
        response = self.client.get(reverse('api_get_halls'), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['halls']), 1)
        self.assertEqual(response.json()['halls'][0]['name'], 'Test Hall')