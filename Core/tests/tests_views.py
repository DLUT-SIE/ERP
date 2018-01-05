from unittest.mock import patch

from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.http import JsonResponse
from rest_framework import status


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dispatch_method_not_allowed(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('Core.views.base.LoginView.post',
           lambda *args, **kwargs: JsonResponse({'status': True}))
    def test_dispatch_method_allowed(self):
        url = reverse('login')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_dispatch_login_succeed(self):
        url = reverse('login')
        data = {
            'username': 'username',
            'password': 'password',
        }
        User.objects.create_user(**data)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_dispatch_login_failed(self):
        url = reverse('login')
        data = {
            'username': 'username',
            'password': 'password',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
