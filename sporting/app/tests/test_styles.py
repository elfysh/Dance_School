import json
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APIClient
from app import models

class StylesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.style = models.Style.objects.create(style_name='Test Style')
        self.admin_user = models.AdminUser.objects.create(username='admin', password='password')
        self.token = self.get_token()

    def get_token(self):
        response = self.client.post(reverse('api_admin_login'), urlencode({'username': 'admin', 'password': 'password'}), content_type='application/x-www-form-urlencoded')
        return response.headers['Token']

    def test_create_style(self):
        data = {
            'style_name': 'New Style'
        }
        response = self.client.post(reverse('api_add_style'), urlencode(data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Style.objects.count(), 2)
        self.assertEqual(models.Style.objects.last().style_name, 'New Style')

    def test_edit_style(self):
        new_data = {
            'style_name': 'Updated Style'
        }
        response = self.client.post(reverse('api_edit_style', args=[self.style.style_id]), urlencode(new_data), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.style.refresh_from_db()
        self.assertEqual(self.style.style_name, 'Updated Style')

    def test_delete_style(self):
        response = self.client.delete(reverse('api_delete_style', args=[self.style.style_id]), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Style.objects.count(), 0)

    def test_get_styles(self):
        response = self.client.get(reverse('api_get_styles'), content_type='application/x-www-form-urlencoded', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['styles']), 1)
        self.assertEqual(response.json()['styles'][0]['name'], 'Test Style')