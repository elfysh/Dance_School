import json
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APIClient
from app import models

class EventsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dance_school = models.DanceSchool.objects.create(
            dance_school_name='Test School',
            dance_school_address='123 Test St',
            phone_number='+7 123 456 78 90'
        )
        self.event = models.Event.objects.create(
            event_name='Test Event',
            dance_school_id=self.dance_school,
            date='2023-10-10',
            description='Test Description'
        )
        self.admin_user = models.AdminUser.objects.create(username='admin', password='password')
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post(reverse('api_admin_login'), urlencode({'username': 'admin', 'password': 'password'}), content_type='application/x-www-form-urlencoded')
        return response.headers['Token']

    def test_create_event(self):
        data = {
            'name': 'New Event',
            'dance_school': self.dance_school.dance_school_id,
            'date': '2023-10-11',
            'description': 'New Description'
        }
        response = self.client.post(reverse('api_add_event'), urlencode(data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Event.objects.count(), 2)
        self.assertEqual(models.Event.objects.last().event_name, 'New Event')

    def test_edit_event(self):
        new_data = {
            'name': 'Updated Event',
            'dance_school': self.dance_school.dance_school_id,
            'date': '2023-10-12',
            'description': 'Updated Description'
        }
        response = self.client.post(reverse('api_edit_event', args=[self.event.event_id]), urlencode(new_data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.event_name, 'Updated Event')

    def test_delete_event(self):
        response = self.client.delete(reverse('api_delete_event', args=[self.event.event_id]), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Event.objects.count(), 0)

    def test_get_events(self):
        response = self.client.get(reverse('api_get_events'), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['events']), 1)
        self.assertEqual(response.json()['events'][0]['name'], 'Test Event')