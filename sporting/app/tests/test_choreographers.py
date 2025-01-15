import json
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APIClient
from app import models

class ChoreographersTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.style = models.Style.objects.create(style_name='Test Style')
        self.choreographer = models.Choreographer.objects.create(
            choreographer_name='Test Choreographer',
            style_id=self.style
        )
        self.admin_user = models.AdminUser.objects.create(username='admin', password='password')
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post(reverse('api_admin_login'), urlencode({'username': 'admin', 'password': 'password'}), content_type='application/x-www-form-urlencoded')
        return response.headers['Token']

    def test_create_choreographer(self):
        data = {
            'choreographer_name': 'New Choreographer',
            'style': self.style.style_id
        }
        response = self.client.post(reverse('api_add_choreographer'), urlencode(data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Choreographer.objects.count(), 2)
        self.assertEqual(models.Choreographer.objects.last().choreographer_name, 'New Choreographer')

    def test_edit_choreographer(self):
        new_data = {
            'choreographer_name': 'Updated Choreographer',
            'style': self.style.style_id
        }
        response = self.client.post(reverse('api_edit_choreographer', args=[self.choreographer.choreographer_id]), urlencode(new_data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.choreographer.refresh_from_db()
        self.assertEqual(self.choreographer.choreographer_name, 'Updated Choreographer')

    def test_delete_choreographer(self):
        response = self.client.delete(reverse('api_delete_choreographer', args=[self.choreographer.choreographer_id]), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Choreographer.objects.count(), 0)

    def test_get_choreographers(self):
        response = self.client.get(reverse('api_get_choreographers'), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()['choreographers'][0]['name'], 'Test Choreographer')