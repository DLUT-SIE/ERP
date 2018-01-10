from unittest.mock import patch, PropertyMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy


class UserAPITest(APITestCase):
    @patch.multiple('Core.serializers.auth.UserCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Core.serializers.auth.UserCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('user-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('user-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_non_production_users(self):
        url = reverse('user-non-production-users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('user-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('Core.api.auth.UserViewSet.get_object',
           lambda *args, **kwargs: mommy.prepare('User'))
    def test_detail(self):
        url = reverse('user-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DepartmentAPITest(APITestCase):
    @patch.multiple('Core.serializers.auth.DepartmentSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Core.serializers.auth.DepartmentSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        # TODO: Should test creation while creation has been tested on
        # serializers.
        mocked_data.return_value = {}
        url = reverse('department-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('department-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_403(self):
        # TODO
        pass

    def test_list(self):
        url = reverse('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Core.models.auth.Department.objects.all',
           lambda: mommy.prepare('Department', _quantity=4))
    def test_list_distribution(self):
        url = reverse('department-distribution')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('department-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('Core.api.auth.DepartmentViewSet.get_object',
           lambda *args, **kwargs: mommy.prepare('Department'))
    def test_detail(self):
        url = reverse('department-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkOrderAPITest(APITestCase):
    def test_list_non_production_plans(self):
        url = reverse('workorder-non-production-plans')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
