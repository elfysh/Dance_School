import json
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APIClient
from app import models

class MasterClassesTests(TestCase):
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
        self.style = models.Style.objects.create(
            style_name='Test Style'
        )
        self.choreographer = models.Choreographer.objects.create(
            choreographer_name='Test Choreographer',
            style_id=self.style
        )
        self.master_class = models.MasterClass.objects.create(
            master_class_name='Test Master Class',
            choreographer_id=self.choreographer,
            hall_id=self.hall,
            time='2023-10-10 10:00:00'
        )
        self.admin_user = models.AdminUser.objects.create(username='admin', password='password')
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post(reverse('api_admin_login'), urlencode({'username': 'admin', 'password': 'password'}), content_type='application/x-www-form-urlencoded')
        return response.headers['Token']

    def test_create_master_class(self):
        data = {
            'name': 'New Master Class',
            'choreographer': self.choreographer.choreographer_id,
            'hall': self.hall.hall_id,
            'date': '2023-10-11',
            'time': '11:00:00'
        }
        response = self.client.post(reverse('api_add_class'), urlencode(data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.MasterClass.objects.count(), 2)
        self.assertEqual(models.MasterClass.objects.last().master_class_name, 'New Master Class')

    def test_edit_master_class(self):
        new_data = {
            'name': 'Updated Master Class',
            'choreographer': self.choreographer.choreographer_id,
            'hall': self.hall.hall_id,
            'date': '2023-10-12',
            'time': '12:00:00'
        }
        response = self.client.post(reverse('api_edit_class', args=[self.master_class.master_class_id]), urlencode(new_data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.master_class.refresh_from_db()
        self.assertEqual(self.master_class.master_class_name, 'Updated Master Class')

    def test_delete_master_class(self):
        response = self.client.delete(reverse('api_delete_class', args=[self.master_class.master_class_id]), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.MasterClass.objects.count(), 0)

    def test_get_master_classes(self):
        response = self.client.get(reverse('api_get_classes'), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['classes']), 1)
        self.assertEqual(response.json()['classes'][0]['name'], 'Test Master Class')