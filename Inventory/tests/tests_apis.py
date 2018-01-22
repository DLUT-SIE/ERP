from unittest.mock import patch, PropertyMock, Mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy


class WeldingMaterialEntryAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.entry'
                    '.WeldingMaterialEntryCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry'
           '.WeldingMaterialEntryCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialentry-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('weldingmaterialentry-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('weldingmaterialentry-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry.WeldingMaterialEntryViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare('WeldingMaterialEntry')
        url = reverse('weldingmaterialentry-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry.WeldingMaterialEntryViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('weldingmaterialentry-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.entry'
                    '.WeldingMaterialEntrySerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry'
           '.WeldingMaterialEntrySerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.entry.WeldingMaterialEntryViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialentry-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialEntryAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.entry'
                    '.SteelMaterialEntryCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry'
           '.SteelMaterialEntryCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialentry-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('steelmaterialentry-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('steelmaterialentry-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry.SteelMaterialEntryViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare('SteelMaterialEntry')
        url = reverse('steelmaterialentry-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry.SteelMaterialEntryViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('steelmaterialentry-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.entry'
                    '.SteelMaterialEntrySerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry'
           '.SteelMaterialEntrySerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.entry.SteelMaterialEntryViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialentry-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuxiliaryMaterialEntryAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.entry'
                    '.AuxiliaryMaterialEntryCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry'
           '.AuxiliaryMaterialEntryCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('auxiliarymaterialentry-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('auxiliarymaterialentry-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('auxiliarymaterialentry-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry.AuxiliaryMaterialEntryViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'AuxiliaryMaterialEntry')
        url = reverse('auxiliarymaterialentry-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry.AuxiliaryMaterialEntryViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('auxiliarymaterialentry-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.entry'
                    '.AuxiliaryMaterialEntrySerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry'
           '.AuxiliaryMaterialEntrySerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.entry.AuxiliaryMaterialEntryViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('auxiliarymaterialentry-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BoughtInComponentEntryAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.entry'
                    '.BoughtInComponentEntryCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry'
           '.BoughtInComponentEntryCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponententry-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('boughtincomponententry-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('boughtincomponententry-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry.BoughtInComponentEntryViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'BoughtInComponentEntry')
        url = reverse('boughtincomponententry-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry.BoughtInComponentEntryViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('boughtincomponententry-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.entry'
                    '.BoughtInComponentEntrySerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry'
           '.BoughtInComponentEntrySerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.entry.BoughtInComponentEntryViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponententry-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeldingMaterialEntryDetailAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.entry_detail'
                    '.WeldingMaterialEntryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry_detail'
           '.WeldingMaterialEntryDetailSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialentrydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('weldingmaterialentrydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('weldingmaterialentrydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_detail'
           '.WeldingMaterialEntryDetailViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'WeldingMaterialEntryDetail')
        url = reverse('weldingmaterialentrydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_detail'
           '.WeldingMaterialEntryDetailViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('weldingmaterialentrydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.entry_detail'
                    '.WeldingMaterialEntryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry_detail'
           '.WeldingMaterialEntryDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.entry_detail'
           '.WeldingMaterialEntryDetailViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialentrydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialEntryDetailAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.entry_detail'
                    '.SteelMaterialEntryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry_detail.'
           'SteelMaterialEntryDetailSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialentrydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('steelmaterialentrydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('steelmaterialentrydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_detail.SteelMaterialEntryDetailViewSet'
           '.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'SteelMaterialEntryDetail')
        url = reverse('steelmaterialentrydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_detail.SteelMaterialEntryDetailViewSet'
           '.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('steelmaterialentrydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.entry_detail'
                    '.SteelMaterialEntryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry_detail'
           '.SteelMaterialEntryDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.entry_detail.SteelMaterialEntryDetailViewSet'
           '.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialentrydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuxiliaryMaterialEntryDetailAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.entry_detail'
                    '.AuxiliaryMaterialEntryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry_detail'
           '.AuxiliaryMaterialEntryDetailSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('auxiliarymaterialentrydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('auxiliarymaterialentrydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('auxiliarymaterialentrydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_detail.AuxiliaryMaterialEntryDetailViewSet'
           '.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'AuxiliaryMaterialEntryDetail')
        url = reverse('auxiliarymaterialentrydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_detail.AuxiliaryMaterialEntryDetailViewSet'
           '.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('auxiliarymaterialentrydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.entry_detail'
                    '.AuxiliaryMaterialEntryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry_detail'
           '.AuxiliaryMaterialEntryDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.entry_detail.AuxiliaryMaterialEntryDetailViewSet'
           '.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('auxiliarymaterialentrydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BoughtInComponentEntryDetailAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.entry_detail'
                    '.BoughtInComponentEntryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry_detail'
           '.BoughtInComponentEntryDetailSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponententrydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('boughtincomponententrydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('boughtincomponententrydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_detail.BoughtInComponentEntryDetailViewSet'
           '.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'BoughtInComponentEntryDetail')
        url = reverse('boughtincomponententrydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_detail.BoughtInComponentEntryDetailViewSet'
           '.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('boughtincomponententrydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.entry_detail'
                    '.BoughtInComponentEntryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.entry_detail'
           '.BoughtInComponentEntryDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.entry_detail.BoughtInComponentEntryDetailViewSet'
           '.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponententrydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeldingMaterialEntryLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('weldingmaterialentryledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_ledger'
           '.WeldingMaterialEntryLedgerViewSet.get_object')
    @patch('Inventory.api.entry_ledger'
           '.WeldingMaterialEntryLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('weldingmaterialentryledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialEntryLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('steelmaterialentryledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_ledger.SteelMaterialEntryLedgerViewSet'
           '.get_object')
    @patch('Inventory.api.entry_ledger'
           '.SteelMaterialEntryLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('steelmaterialentryledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuxiliaryMaterialEntryLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('auxiliarymaterialentryledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_ledger'
           '.AuxiliaryMaterialEntryLedgerViewSet.get_object')
    @patch('Inventory.api.entry_ledger'
           '.AuxiliaryMaterialEntryLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('auxiliarymaterialentryledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BoughtInComponentEntryLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('boughtincomponententryledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.entry_ledger'
           '.BoughtInComponentEntryLedgerViewSet.get_object')
    @patch('Inventory.api.entry_ledger'
           '.BoughtInComponentEntryLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('boughtincomponententryledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeldingMaterialInventoryDetailAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.inventory_detail'
                    '.WeldingMaterialInventoryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.inventory_detail'
           '.WeldingMaterialInventoryDetailSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialinventorydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('weldingmaterialinventorydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('weldingmaterialinventorydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_detail'
           '.WeldingMaterialInventoryDetailViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'WeldingMaterialInventoryDetail')
        url = reverse('weldingmaterialinventorydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_detail'
           '.WeldingMaterialInventoryDetailViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('weldingmaterialinventorydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.inventory_detail'
                    '.WeldingMaterialInventoryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.inventory_detail'
           '.WeldingMaterialInventoryDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.inventory_detail'
           '.WeldingMaterialInventoryDetailViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialinventorydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialInventoryDetailAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.inventory_detail'
                    '.SteelMaterialInventoryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.inventory_detail.'
           'SteelMaterialInventoryDetailSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialinventorydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('steelmaterialinventorydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('steelmaterialinventorydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_detail.SteelMaterialInventoryDetailViewSet'
           '.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'SteelMaterialInventoryDetail')
        url = reverse('steelmaterialinventorydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_detail.SteelMaterialInventoryDetailViewSet'
           '.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('steelmaterialinventorydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.inventory_detail'
                    '.SteelMaterialInventoryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.inventory_detail'
           '.SteelMaterialInventoryDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.inventory_detail.SteelMaterialInventoryDetailViewSet'
           '.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialinventorydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuxiliaryMaterialInventoryDetailAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.inventory_detail'
                    '.AuxiliaryMaterialInventoryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.inventory_detail'
           '.AuxiliaryMaterialInventoryDetailSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('auxiliarymaterialinventorydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('auxiliarymaterialinventorydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('auxiliarymaterialinventorydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_detail'
           '.AuxiliaryMaterialInventoryDetailViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'AuxiliaryMaterialInventoryDetail')
        url = reverse('auxiliarymaterialinventorydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_detail'
           '.AuxiliaryMaterialInventoryDetailViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('auxiliarymaterialinventorydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.inventory_detail'
                    '.AuxiliaryMaterialInventoryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.inventory_detail'
           '.AuxiliaryMaterialInventoryDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.inventory_detail'
           '.AuxiliaryMaterialInventoryDetailViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('auxiliarymaterialinventorydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BoughtInComponentInventoryDetailAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.inventory_detail'
                    '.BoughtInComponentInventoryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.inventory_detail'
           '.BoughtInComponentInventoryDetailSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponentinventorydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('boughtincomponentinventorydetail-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('boughtincomponentinventorydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_detail'
           '.BoughtInComponentInventoryDetailViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'BoughtInComponentInventoryDetail')
        url = reverse('boughtincomponentinventorydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_detail'
           '.BoughtInComponentInventoryDetailViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('boughtincomponentinventorydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.inventory_detail'
                    '.BoughtInComponentInventoryDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.inventory_detail'
           '.BoughtInComponentInventoryDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.inventory_detail'
           '.BoughtInComponentInventoryDetailViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponentinventorydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeldingMaterialInventoryLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('weldingmaterialinventoryledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_ledger'
           '.WeldingMaterialInventoryLedgerViewSet.get_object')
    @patch('Inventory.api.inventory_ledger'
           '.WeldingMaterialInventoryLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('weldingmaterialinventoryledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialInventoryLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('steelmaterialinventoryledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_ledger'
           '.SteelMaterialInventoryLedgerViewSet.get_object')
    @patch('Inventory.api.inventory_ledger'
           '.SteelMaterialInventoryLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('steelmaterialinventoryledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuxiliaryMaterialInventoryLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('auxiliarymaterialinventoryledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_ledger'
           '.AuxiliaryMaterialInventoryLedgerViewSet.get_object')
    @patch('Inventory.api.inventory_ledger'
           '.AuxiliaryMaterialInventoryLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('auxiliarymaterialinventoryledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BoughtInComponentInventoryLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('boughtincomponentinventoryledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.inventory_ledger'
           '.BoughtInComponentInventoryLedgerViewSet.get_object')
    @patch('Inventory.api.inventory_ledger'
           '.BoughtInComponentInventoryLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('boughtincomponentinventoryledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeldingMaterialApplyCardAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.apply'
                    '.WeldingMaterialApplyCardCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply'
           '.WeldingMaterialApplyCardCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialapplycard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('weldingmaterialapplycard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('weldingmaterialapplycard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply.WeldingMaterialApplyCardViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'WeldingMaterialApplyCard')
        url = reverse('weldingmaterialapplycard-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply.WeldingMaterialApplyCardViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('weldingmaterialapplycard-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.apply'
                    '.WeldingMaterialApplyCardSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply'
           '.WeldingMaterialApplyCardSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.apply.WeldingMaterialApplyCardViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialapplycard-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialApplyCardAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.apply'
                    '.SteelMaterialApplyCardCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply'
           '.SteelMaterialApplyCardCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialapplycard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('steelmaterialapplycard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('steelmaterialapplycard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply.SteelMaterialApplyCardViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'SteelMaterialApplyCard')
        url = reverse('steelmaterialapplycard-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply.SteelMaterialApplyCardViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('steelmaterialapplycard-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.apply'
                    '.SteelMaterialApplyCardSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply'
           '.SteelMaterialApplyCardSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.apply.SteelMaterialApplyCardViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialapplycard-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuxiliaryMaterialApplyCardAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.apply'
                    '.AuxiliaryMaterialApplyCardCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply'
           '.AuxiliaryMaterialApplyCardCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('auxiliarymaterialapplycard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('auxiliarymaterialapplycard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('auxiliarymaterialapplycard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply.AuxiliaryMaterialApplyCardViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'AuxiliaryMaterialApplyCard')
        url = reverse('auxiliarymaterialapplycard-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply.AuxiliaryMaterialApplyCardViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('auxiliarymaterialapplycard-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.apply'
                    '.AuxiliaryMaterialApplyCardSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply'
           '.AuxiliaryMaterialApplyCardSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.apply.AuxiliaryMaterialApplyCardViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('auxiliarymaterialapplycard-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BoughtInComponentApplyCardAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.apply'
                    '.BoughtInComponentApplyCardCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply'
           '.BoughtInComponentApplyCardCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponentapplycard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('boughtincomponentapplycard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('boughtincomponentapplycard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply.BoughtInComponentApplyCardViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'BoughtInComponentApplyCard')
        url = reverse('boughtincomponentapplycard-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply.BoughtInComponentApplyCardViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('boughtincomponentapplycard-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.apply'
                    '.BoughtInComponentApplyCardSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply'
           '.BoughtInComponentApplyCardSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.apply.BoughtInComponentApplyCardViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponentapplycard-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialApplyDetailAPITest(APITestCase):
    def test_create(self):
        url = reverse('steelmaterialapplydetail-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        url = reverse('steelmaterialapplydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list(self):
        url = reverse('steelmaterialapplydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply_detail.SteelMaterialApplyDetailViewSet'
           '.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'SteelMaterialApplyDetail')
        url = reverse('steelmaterialapplydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.multiple('Inventory.serializers.apply_detail'
                    '.SteelMaterialApplyDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply_detail'
           '.SteelMaterialApplyDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.apply_detail.SteelMaterialApplyDetailViewSet'
           '.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialapplydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BoughtInComponentApplyDetailAPITest(APITestCase):
    def test_create(self):
        url = reverse('boughtincomponentapplydetail-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        url = reverse('boughtincomponentapplydetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list(self):
        url = reverse('boughtincomponentapplydetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply_detail.BoughtInComponentApplyDetailViewSet'
           '.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'BoughtInComponentApplyDetail')
        url = reverse('boughtincomponentapplydetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.multiple('Inventory.serializers.apply_detail'
                    '.BoughtInComponentApplyDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.apply_detail'
           '.BoughtInComponentApplyDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.apply_detail.BoughtInComponentApplyDetailViewSet'
           '.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponentapplydetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeldingMaterialApplyLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('weldingmaterialapplyledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply_ledger'
           '.WeldingMaterialApplyLedgerViewSet.get_object')
    @patch('Inventory.api.apply_ledger'
           '.WeldingMaterialApplyLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('weldingmaterialapplyledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialApplyLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('steelmaterialapplyledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply_ledger.SteelMaterialApplyLedgerViewSet'
           '.get_object')
    @patch('Inventory.api.apply_ledger'
           '.SteelMaterialApplyLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('steelmaterialapplyledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuxiliaryMaterialApplyLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('auxiliarymaterialapplyledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply_ledger'
           '.AuxiliaryMaterialApplyLedgerViewSet.get_object')
    @patch('Inventory.api.apply_ledger'
           '.AuxiliaryMaterialApplyLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('auxiliarymaterialapplyledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BoughtInComponentApplyLedgerAPITest(APITestCase):
    def test_list(self):
        url = reverse('boughtincomponentapplyledger-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.apply_ledger'
           '.BoughtInComponentApplyLedgerViewSet.get_object')
    @patch('Inventory.api.apply_ledger'
           '.BoughtInComponentApplyLedgerViewSet.get_serializer')
    def test_detail(self, mocked_get_serializer, mocked_get_object):
        mocked_get_object.return_value = Mock()
        serializer = Mock(data={})
        mocked_get_serializer.return_value = serializer
        url = reverse('boughtincomponentapplyledger-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeldingMaterialRefundCardAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.refund'
                    '.WeldingMaterialRefundCardCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.refund'
           '.WeldingMaterialRefundCardCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialrefundcard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('weldingmaterialrefundcard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('weldingmaterialrefundcard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.refund.WeldingMaterialRefundCardViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'WeldingMaterialRefundCard')
        url = reverse('weldingmaterialrefundcard-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.refund.WeldingMaterialRefundCardViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('weldingmaterialrefundcard-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.refund'
                    '.WeldingMaterialRefundCardSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.refund'
           '.WeldingMaterialRefundCardSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.refund.WeldingMaterialRefundCardViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialrefundcard-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialRefundCardAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.refund'
                    '.SteelMaterialRefundCardCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.refund'
           '.SteelMaterialRefundCardCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialrefundcard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('steelmaterialrefundcard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('steelmaterialrefundcard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.refund.SteelMaterialRefundCardViewSet.get_object')
    @patch('Inventory.serializers.refund'
           '.SteelMaterialRefundCardSerializer.data',
           new_callable=PropertyMock)
    def test_detail(self, mocked_data, mocked_get_object):
        mocked_data.return_value = {}
        mocked_get_object.return_value = mommy.prepare(
            'SteelMaterialRefundCard')
        url = reverse('steelmaterialrefundcard-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.refund.SteelMaterialRefundCardViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('steelmaterialrefundcard-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.refund'
                    '.SteelMaterialRefundCardSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.refund'
           '.SteelMaterialRefundCardSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.refund.SteelMaterialRefundCardViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('steelmaterialrefundcard-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BoughtInComponentRefundCardAPITest(APITestCase):
    @patch.multiple('Inventory.serializers.refund'
                    '.BoughtInComponentRefundCardCreateSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.refund'
           '.BoughtInComponentRefundCardCreateSerializer.data',
           new_callable=PropertyMock)
    def test_create_201(self, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponentrefundcard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_400(self):
        url = reverse('boughtincomponentrefundcard-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        url = reverse('boughtincomponentrefundcard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.refund'
           '.BoughtInComponentRefundCardViewSet.get_object')
    def test_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'BoughtInComponentRefundCard')
        url = reverse('boughtincomponentrefundcard-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.refund'
           '.BoughtInComponentRefundCardViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('boughtincomponentrefundcard-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.multiple('Inventory.serializers.refund'
                    '.BoughtInComponentRefundCardSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.refund'
           '.BoughtInComponentRefundCardSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.refund'
           '.BoughtInComponentRefundCardViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boughtincomponentrefundcard-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SteelMaterialRefundDetailAPITest(APITestCase):
    def test_board_delete(self):
        url = reverse('boardsteelmaterialrefunddetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_bar_delete(self):
        url = reverse('barsteelmaterialrefunddetail-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('Inventory.api.refund_detail.BoardSteelMaterialRefundDetailViewSet'
           '.get_object')
    def test_board_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'BoardSteelMaterialRefundDetail')
        url = reverse('boardsteelmaterialrefunddetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.refund_detail.BarSteelMaterialRefundDetailViewSet'
           '.get_object')
    def test_bar_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'BarSteelMaterialRefundDetail')
        url = reverse('barsteelmaterialrefunddetail-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.multiple('Inventory.serializers.refund_detail'
                    '.BoardSteelMaterialRefundDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.refund_detail'
           '.BoardSteelMaterialRefundDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.refund_detail.BoardSteelMaterialRefundDetailViewSet'
           '.get_object')
    def test_board_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('boardsteelmaterialrefunddetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.multiple('Inventory.serializers.refund_detail'
                    '.BarSteelMaterialRefundDetailSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.refund_detail'
           '.BarSteelMaterialRefundDetailSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.refund_detail.BarSteelMaterialRefundDetailViewSet'
           '.get_object')
    def test_bar_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('barsteelmaterialrefunddetail-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WarehouseViewSetTest(APITestCase):
    def test_list(self):
        url = reverse('warehouse-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.other.WarehouseViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('warehouse-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch('Inventory.api.other.WarehouseViewSet.get_object')
    def test_bar_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'Warehouse')
        url = reverse('warehouse-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.multiple('Inventory.serializers.other'
                    '.WarehouseSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.other'
           '.WarehouseSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.other.WarehouseViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('warehouse-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeldingMaterialHumitureRecordViewSetTest(APITestCase):
    def test_list(self):
        url = reverse('weldingmaterialhumiturerecord-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.other'
           '.WeldingMaterialHumitureRecordViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('weldingmaterialhumiturerecord-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch('Inventory.api.other'
           '.WeldingMaterialHumitureRecordViewSet.get_object')
    def test_bar_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'WeldingMaterialHumitureRecord')
        url = reverse('weldingmaterialhumiturerecord-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.multiple('Inventory.serializers.other'
                    '.WeldingMaterialHumitureRecordSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.other'
           '.WeldingMaterialHumitureRecordSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.other'
           '.WeldingMaterialHumitureRecordViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialhumiturerecord-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeldingMaterialBakeRecordViewSetTest(APITestCase):
    def test_list(self):
        url = reverse('weldingmaterialbakerecord-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('Inventory.api.other'
           '.WeldingMaterialBakeRecordViewSet.get_object')
    def test_delete(self, mocked_get_object):
        url = reverse('weldingmaterialbakerecord-detail', args=('1',))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch('Inventory.api.other'
           '.WeldingMaterialBakeRecordViewSet.get_object')
    def test_bar_detail(self, mocked_get_object):
        mocked_get_object.return_value = mommy.prepare(
            'WeldingMaterialBakeRecord')
        url = reverse('weldingmaterialbakerecord-detail', args=('1',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.multiple('Inventory.serializers.other'
                    '.WeldingMaterialBakeRecordSerializer',
                    is_valid=lambda *args, **kwargs: True,
                    save=lambda *args, **kwargs: None)
    @patch('Inventory.serializers.other'
           '.WeldingMaterialBakeRecordSerializer.data',
           new_callable=PropertyMock)
    @patch('Inventory.api.other'
           '.WeldingMaterialBakeRecordViewSet.get_object')
    def test_update(self, mocked_get_object, mocked_data):
        mocked_data.return_value = {}
        url = reverse('weldingmaterialbakerecord-detail', args=('1',))
        data = {}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
