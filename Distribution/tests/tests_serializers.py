from unittest.mock import patch, Mock

from django.test import TestCase
from model_mommy import mommy

import Distribution.serializers.product as product_serializers


@patch('Core.models.auth.Department.distribution.get',
       lambda: mommy.prepare('Department', group__name='distribution'))
@patch('Core.models.auth.Department.process.get',
       lambda: mommy.prepare('Department', group__name='process'))
@patch('Core.models.auth.Department.procurement.get',
       lambda: mommy.prepare('Department', group__name='procurement'))
@patch('Core.models.auth.Department.production.get',
       lambda: mommy.prepare('Department', group__name='production'))
@patch('Distribution.serializers.product.ProductSerializer.get_actions',
       lambda *args: {})
class ProductSerializerTest(TestCase):
    def test_get_departments(self):
        serializer = product_serializers.ProductSerializer()
        departments = serializer.get_departments()
        self.assertEqual(len(departments), 4)

    @patch('Distribution.serializers.product.BiddingDocumentSimpleSerializer')
    @patch('Distribution.models.BiddingDocument.objects.filter')
    def test_get_documents_from_distribution(self, mocked_filter,
                                             mocked_serializer):
        mocked_serializer.return_value.data = 'document'
        mocked_filter.filter.return_value = mommy.prepare('BiddingDocument')
        serializer = product_serializers.ProductSerializer()
        serializer.context['request'] = Mock()
        product = mommy.prepare('Product')
        documents = serializer.get_documents_from_distribution(product)
        self.assertEqual(len(documents), 3)

    @patch('Distribution.serializers.product.BiddingDocumentSimpleSerializer')
    @patch('Distribution.models.BiddingDocument.objects.filter')
    def test_get_documents_to_distribution(self, mocked_filter,
                                           mocked_serializer):
        mocked_serializer.return_value.data = 'document'
        _mocked_filter = Mock()
        _mocked_filter.filter.return_value = []
        mocked_filter.return_value = _mocked_filter
        serializer = product_serializers.ProductSerializer()
        product = mommy.prepare('Product')
        documents = serializer.get_documents_to_distribution(product)
        self.assertEqual(len(documents), 3)

    def test_product_serializer_fields(self):
        serializer = product_serializers.ProductSerializer()
        expected_keys = {
            'id', 'name', 'terminated', 'status', 'actions', 'pretty_status',
            'documents_from_distribution', 'documents_to_distribution'}
        self.assertEqual(expected_keys, set(serializer.fields.keys()))

    def test_product_list_serializer_fields(self):
        serializer = product_serializers.ProductListSerializer()
        expected_keys = {'id', 'name', 'documents_from_distribution',
                         'documents_to_distribution'}
        self.assertEqual(expected_keys, set(serializer.fields.keys()))

    @patch('Distribution.serializers.product.BiddingDocumentSimpleSerializer')
    @patch('Distribution.models.BiddingDocument.objects.filter')
    def test_product_simple_serializer_get_documents(
            self, mocked_filter, mocked_serializer):
        mocked_serializer.return_value.data = 'document'
        _mocked_filter = Mock()
        _mocked_filter.filter.return_value = []
        mocked_filter.return_value = _mocked_filter
        serializer = product_serializers.ProductSimpleSerializer()
        serializer.context['department'] = Mock()
        product = mommy.prepare('Product')
        documents = serializer.get_documents_from_distribution(product)
        self.assertEqual(len(documents), 1)
        documents = serializer.get_documents_to_distribution(product)
        self.assertEqual(len(documents), 1)

    def test_product_update_serializer_fields(self):
        serializer = product_serializers.ProductUpdateSerializer()
        expected_keys = {
            'id', 'name', 'terminated', 'status', 'actions', 'pretty_status',
            'documents_from_distribution', 'documents_to_distribution'}
        self.assertEqual(expected_keys, set(serializer.fields.keys()))

    def test_product_create_serializer_fields(self):
        serializer = product_serializers.ProductCreateSerializer()
        expected_keys = {
            'id', 'name', 'terminated', 'status', 'actions', 'pretty_status',
            'documents_from_distribution', 'documents_to_distribution'}
        self.assertEqual(expected_keys, set(serializer.fields.keys()))


@patch('Distribution.serializers.product.ProductSerializer.get_actions',
       lambda *args: {})
class BiddingDocumentSerializerTest(TestCase):
    def test_bidding_document_simple_serializer_fields(self):
        serializer = product_serializers.BiddingDocumentSimpleSerializer()
        expected_keys = {'id', 'path', 'name', 'pretty_status', 'actions'}
        self.assertEqual(expected_keys, set(serializer.fields.keys()))

    def test_bidding_document_serializer_fields(self):
        serializer = product_serializers.BiddingDocumentSerializer()
        expected_keys = {
            'id', 'path', 'name', 'pretty_status', 'actions',
            'src', 'dst', 'status', 'upload_dt', 'product'}
        self.assertEqual(expected_keys, set(serializer.fields.keys()))

    def test_bidding_document_update_serializer_fields(self):
        serializer = product_serializers.BiddingDocumentUpdateSerializer()
        expected_keys = {
            'id', 'path', 'name', 'pretty_status', 'actions',
            'src', 'dst', 'status', 'upload_dt', 'product'}
        self.assertEqual(expected_keys, set(serializer.fields.keys()))

    @patch('Distribution.models.BiddingDocument.objects.get_or_create')
    def test_bidding_document_serializer_create_created(self, mocked_create):
        serializer = product_serializers.BiddingDocumentSerializer()
        validated_data = {
            'product': 'product',
            'src': 'src',
            'dst': 'dst',
            'path': 'path',
        }
        mock_obj = Mock()
        mocked_create.return_value = (mock_obj, True)
        serializer.create(validated_data)
        mock_obj.save.assert_called()

    @patch('Distribution.models.BiddingDocument.objects.get_or_create')
    def test_bidding_document_serializer_create_updated(self, mocked_create):
        serializer = product_serializers.BiddingDocumentSerializer()
        path = Mock()
        validated_data = {
            'product': 'product',
            'src': 'src',
            'dst': 'dst',
            'path': path,
        }
        mocked_obj = Mock()
        mocked_obj.path = path
        mocked_create.return_value = (mocked_obj, False)
        serializer.create(validated_data)
        mocked_obj.path.delete.assert_called()
        mocked_obj.save.assert_called()
