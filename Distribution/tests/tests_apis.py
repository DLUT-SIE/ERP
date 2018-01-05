from unittest.mock import patch, Mock

from django.urls import reverse
from rest_framework import status, serializers
from rest_framework.test import APITestCase


class ProductAPITest(APITestCase):
    @patch('Distribution.serializers.ProductCreateSerializer')
    def test_create_product(self, mocked_serializer_cls):
        url = reverse('product-list')
        mocked_serializer = Mock()
        mocked_serializer.is_valid.side_effect = serializers.ValidationError()
        mocked_serializer_cls.return_value = mocked_serializer
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Distribution.serializers.ProductSerializer')
    @patch('Distribution.api.product.ProductViewSet.get_object')
    def test_get_product(self, mocked_object_mehotd, mocked_serializer_cls):
        url = reverse('product-detail', args=('1',))
        mocked_serializer = Mock()
        mocked_serializer.data = {}
        mocked_serializer_cls.return_value = mocked_serializer
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Distribution.api.product.ProductViewSet.get_object')
    def test_delete_product(self, mocked_object_mehotd):
        item_url = reverse('product-detail', args=('1',))
        response = self.client.delete(item_url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('Distribution.serializers.ProductUpdateSerializer')
    @patch('Distribution.api.product.ProductViewSet.get_object')
    def test_update_product(self, mocked_object_mehotd, mocked_serializer_cls):
        url = reverse('product-detail', args=('1',))
        mocked_serializer = Mock()
        mocked_serializer.is_valid.side_effect = serializers.ValidationError()
        mocked_serializer_cls.return_value = mocked_serializer
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('Distribution.serializers.ProductSimpleSerializer')
    @patch('Distribution.api.product.ProductViewSet.get_object')
    @patch('Distribution.api.product.get_object_or_404')
    def test_get_product_list_simple(self, mock_obj_or_404,
                                     mocked_object_mehotd,
                                     mocked_serializer_cls):
        url = reverse('product-list')
        mocked_serializer = Mock()
        mocked_serializer.data = {}
        mocked_serializer_cls.return_value = mocked_serializer

        response = self.client.get(url, {'department': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BiddingDocumentAPITest(APITestCase):
    @patch('Distribution.serializers.BiddingDocumentSerializer')
    def test_create_bidding_document(self, mocked_serializer_cls):
        url = reverse('biddingdocument-list')
        mocked_serializer = Mock()
        mocked_serializer.is_valid.side_effect = serializers.ValidationError()
        mocked_serializer_cls.return_value = mocked_serializer
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('Distribution.serializers.BiddingDocumentSerializer')
    @patch('Distribution.api.product.BiddingDocumentViewSet.get_object')
    def test_get_bidding_document(self, mocked_object_mehotd,
                                  mocked_serializer_cls):
        url = reverse('biddingdocument-detail', args=('1',))
        mocked_serializer = Mock()
        mocked_serializer.data = {}
        mocked_serializer_cls.return_value = mocked_serializer
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Distribution.serializers.BiddingDocumentUpdateSerializer')
    @patch('Distribution.api.product.BiddingDocumentViewSet.get_object')
    def test_update_bidding_document(self, mocked_object_mehotd,
                                     mocked_serializer_cls):
        url = reverse('biddingdocument-detail', args=('1',))
        mocked_serializer = Mock()
        mocked_serializer.is_valid.side_effect = serializers.ValidationError()
        mocked_serializer_cls.return_value = mocked_serializer
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
