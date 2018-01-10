from unittest.mock import patch, PropertyMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy


class ProductAPITest(APITestCase):
    @patch.multiple('Distribution.serializers.product'
                    '.ProductCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Distribution.serializers.product'
           '.ProductCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('product-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('product-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.multiple('Distribution.serializers.product'
                    '.ProductSerializer',
                    get_documents_from_distribution=lambda *args: {},
                    get_documents_to_distribution=lambda *args: {})
    @patch('Distribution.api.product.ProductViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare('Product')
        url = reverse('product-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Distribution.api.product.ProductViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('product-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch.multiple('Distribution.serializers.product'
                    '.ProductSerializer',
                    get_documents_from_distribution=lambda *args: {},
                    get_documents_to_distribution=lambda *args: {})
    @patch('Distribution.api.product.ProductViewSet.get_object')
    def test_update(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare('Product')
        url = reverse('product-detail', args=('1',))
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Distribution.api.product'
           '.ProductViewSet.get_serializer_context')
    def test_list_simple(self, mocked_get_serializer_context):
        url = reverse('product-list')
        response = self.client.get(url, {'department': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BiddingDocumentAPITest(APITestCase):
    @patch.multiple('Distribution.serializers.product'
                    '.BiddingDocumentSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Distribution.serializers.product'
           '.BiddingDocumentSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('biddingdocument-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('biddingdocument-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('Distribution.api.product.BiddingDocumentViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare('BiddingDocument')
        url = reverse('biddingdocument-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.multiple('Distribution.serializers.product'
                    '.BiddingDocumentSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Distribution.serializers.product'
           '.BiddingDocumentSerializer.data',
           new_callable=PropertyMock)
    @patch('Distribution.api.product.BiddingDocumentViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('biddingdocument-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
