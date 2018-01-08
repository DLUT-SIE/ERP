from unittest.mock import patch, Mock

from django.test import TestCase
from django.utils.timezone import now
from rest_framework import serializers
from model_mommy import mommy

import Inventory.serializers.entry as entry_serializers
import Inventory.serializers.entry_detail as entry_detail_serializers
import Inventory.serializers.entry_ledger as ledger_serializers
import Inventory.serializers.inventory_detail as in_detail_serializers
import Inventory.serializers.inventory_ledger as in_ledger_serializers


class WeldingMaterialEntrySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry = mommy.prepare('WeldingMaterialEntry')

    @patch('Inventory.serializers.entry.WeldingMaterialEntrySerializer'
           '.get_actions')
    def test_welding_material_entry_serializer_fields(self,
                                                      mocked_get_actions):
        mocked_get_actions.return_value = {}
        data = entry_serializers.WeldingMaterialEntrySerializer(
            self.entry).data
        expected_keys = {'id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                         'purchaser', 'inspector', 'keeper', 'status',
                         'pretty_status', 'details', 'actions'}
        self.assertEqual(set(data.keys()), expected_keys)

    def test_welding_material_entry_list_serializer_fields(self):
        data = entry_serializers.WeldingMaterialEntryListSerializer(
            self.entry).data
        expected_keys = {'id', 'uid', 'create_dt', 'purchaser', 'inspector',
                         'status', 'pretty_status'}
        self.assertEqual(set(data.keys()), expected_keys)

    def test_welding_material_entry_create_serializer_fields(self):
        data = entry_serializers.WeldingMaterialEntryCreateSerializer(
            self.entry).data
        expected_keys = set()
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Procurement.models.other.ArrivalInspection.objects.filter')
    def test_entry_create_serializer_validate_inspections(self,
                                                          mocked_filter):
        inspection_ids = [1, 2, 3]
        mocked_filter.return_value = []
        serializer = entry_serializers.WeldingMaterialEntryCreateSerializer()
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_inspections(inspection_ids)
        mocked_queryset = Mock()
        mocked_filter.return_value = mocked_queryset
        mocked_queryset.count.return_value = 2
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_inspections(inspection_ids)
        mocked_queryset.count.return_value = 3
        self.assertIs(serializer.validate_inspections(inspection_ids),
                      mocked_queryset)

    @patch('Procurement.models.bidding.BiddingSheet.objects.filter')
    def test_entry_create_serializer_validate_bidding_sheet(self,
                                                            mocked_filter):
        bidding_sheet_id = 1
        mocked_filter.return_value = []
        serializer = entry_serializers.WeldingMaterialEntryCreateSerializer()
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_bidding_sheet(bidding_sheet_id)
        mocked_bidding_sheet = [mommy.prepare('BiddingSheet')]
        mocked_filter.return_value = mocked_bidding_sheet
        self.assertIs(serializer.validate_bidding_sheet(bidding_sheet_id),
                      mocked_bidding_sheet[0])

    @patch('Inventory.models.entry.WeldingMaterialEntry.create_entry')
    def test_entry_create_serializer_create_fields(self, mocked_create_entry):
        serializer = entry_serializers.WeldingMaterialEntryCreateSerializer()
        serializer.create({})
        mocked_create_entry.assert_called()


class SteelMaterialEntrySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry = mommy.prepare('SteelMaterialEntry')

    @patch('Inventory.serializers.entry.SteelMaterialEntrySerializer'
           '.get_actions')
    def test_steel_material_entry_serializer_fields(self, mocked_get_actions):
        mocked_get_actions.return_value = {}
        data = entry_serializers.SteelMaterialEntrySerializer(self.entry).data
        expected_keys = {'id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                         'purchaser', 'inspector', 'keeper', 'status',
                         'pretty_status', 'details', 'actions'}
        self.assertEqual(set(data.keys()), expected_keys)

    def test_steel_material_entry_list_serializer_fields(self):
        data = entry_serializers.SteelMaterialEntryListSerializer(
            self.entry).data
        expected_keys = {'id', 'uid', 'create_dt', 'purchaser', 'inspector',
                         'steel_type', 'pretty_steel_type',
                         'status', 'pretty_status'}
        self.assertEqual(set(data.keys()), expected_keys)


class AuxiliaryMaterialEntrySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry = mommy.prepare('AuxiliaryMaterialEntry')

    @patch('Inventory.serializers.entry.AuxiliaryMaterialEntrySerializer'
           '.get_actions')
    def test_auxiliary_material_entry_serializer_fields(self,
                                                        mocked_get_actions):
        mocked_get_actions.return_value = {}
        data = entry_serializers.AuxiliaryMaterialEntrySerializer(
            self.entry).data
        expected_keys = {'id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                         'purchaser', 'inspector', 'keeper', 'status',
                         'pretty_status', 'details', 'actions'}
        self.assertEqual(set(data.keys()), expected_keys)

    def test_auxiliary_material_entry_list_serializer_fields(self):
        data = entry_serializers.AuxiliaryMaterialEntryListSerializer(
            self.entry).data
        expected_keys = {'id', 'uid', 'create_dt', 'purchaser', 'inspector',
                         'status', 'pretty_status'}
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentEntrySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry = mommy.prepare('BoughtInComponentEntry')

    @patch('Inventory.serializers.entry.BoughtInComponentEntrySerializer'
           '.get_actions')
    def test_bought_in_component_entry_serializer_fields(self,
                                                         mocked_get_actions):
        mocked_get_actions.return_value = {}
        data = entry_serializers.BoughtInComponentEntrySerializer(
            self.entry).data
        expected_keys = {'id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                         'source', 'category', 'pretty_category',
                         'purchaser', 'inspector', 'keeper', 'status',
                         'pretty_status', 'details', 'actions'}
        self.assertEqual(set(data.keys()), expected_keys)

    def test_bought_in_component_entry_list_serializer_fields(self):
        data = entry_serializers.BoughtInComponentEntryListSerializer(
            self.entry).data
        expected_keys = {'id', 'uid', 'create_dt', 'source', 'pretty_category',
                         'purchaser', 'status', 'pretty_status'}
        self.assertEqual(set(data.keys()), expected_keys)


class WeldingMaterialEntryDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry_detail = mommy.prepare('WeldingMaterialEntryDetail')

    def test_detail_serializer_fields(self):
        data = entry_detail_serializers.WeldingMaterialEntryDetailSerializer(
            self.entry_detail).data
        expected_keys = {
            'id', 'entry', 'procurement_material', 'weight', 'count',
            'unit', 'factory', 'remark', 'production_dt',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class SteelMaterialEntryDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry_detail = mommy.prepare('SteelMaterialEntryDetail')

    def test_detail_serializer_fields(self):
        data = entry_detail_serializers.SteelMaterialEntryDetailSerializer(
            self.entry_detail).data
        expected_keys = {
            'id', 'entry', 'procurement_material', 'weight', 'count',
            'unit', 'factory', 'remark', 'length',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class AuxiliaryMaterialEntryDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry_detail = mommy.prepare('AuxiliaryMaterialEntryDetail')

    def test_detail_serializer_fields(self):
        data = entry_detail_serializers.AuxiliaryMaterialEntryDetailSerializer(
            self.entry_detail).data
        expected_keys = {
            'id', 'entry', 'procurement_material', 'weight', 'count',
            'unit', 'factory', 'remark',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentEntryDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry_detail = mommy.prepare('BoughtInComponentEntryDetail')

    def test_detail_serializer_fields(self):
        data = entry_detail_serializers.BoughtInComponentEntryDetailSerializer(
            self.entry_detail).data
        expected_keys = {
            'id', 'entry', 'procurement_material', 'weight', 'count',
            'unit', 'factory', 'remark',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class WeldingMaterialEntryLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry_detail = mommy.prepare(
            'WeldingMaterialEntryDetail',
            procurement_material__process_material__material__uid=123)

    def test_ledger_serializer_fields(self):
        data = ledger_serializers.WeldingMaterialEntryLedgerSerializer(
            self.entry_detail).data
        expected_keys = {
            'id', 'material_mark', 'specification', 'entry_dt',
            'material_number', 'factory', 'count', 'weight',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class SteelMaterialEntryLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry_detail = mommy.prepare(
            'SteelMaterialEntryDetail',
            procurement_material__process_material__material__uid=123,
            entry__bidding_sheet__purchase_order__work_order__uid=123)

    def test_ledger_serializer_fields(self):
        data = ledger_serializers.SteelMaterialEntryLedgerSerializer(
            self.entry_detail).data
        expected_keys = {
            'id', 'material', 'specification', 'entry_dt',
            'material_number', 'work_order_uid', 'count', 'weight',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class AuxiliaryMaterialEntryLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry_detail = mommy.prepare(
            'AuxiliaryMaterialEntryDetail',
            procurement_material__process_material__spec='spec',
            entry__create_dt=now())

    def test_ledger_serializer_fields(self):
        data = ledger_serializers.AuxiliaryMaterialEntryLedgerSerializer(
            self.entry_detail).data
        expected_keys = {
            'id', 'specification', 'entry_dt',
            'entry_uid', 'factory', 'supplier', 'count',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentEntryLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry_detail = mommy.prepare(
            'BoughtInComponentEntryDetail',
            procurement_material__process_material__material__name='name',
            entry__bidding_sheet__purchase_order__work_order__uid=123)

    def test_ledger_serializer_fields(self):
        data = ledger_serializers.BoughtInComponentEntryLedgerSerializer(
            self.entry_detail).data
        expected_keys = {
            'id', 'work_order_uid', 'specification', 'material',
            'entry_dt', 'material_number', 'entry_uid', 'count',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class WeldingMaterialInventoryDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inventory_detail = mommy.prepare(
            'WeldingMaterialInventoryDetail',
            entry_detail__unit='unit',
        )

    def test_inventory_detail_fields(self):
        data = in_detail_serializers.WeldingMaterialInventoryDetailSerializer(
            self.inventory_detail).data
        expected_keys = {
            'id', 'entry_detail', 'deadline', 'weight', 'count',
            'unit', 'status', 'pretty_status',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class SteelMaterialInventoryDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inventory_detail = mommy.prepare(
            'SteelMaterialInventoryDetail',
            entry_detail__unit='unit',
        )

    def test_inventory_detail_fields(self):
        data = in_detail_serializers.SteelMaterialInventoryDetailSerializer(
            self.inventory_detail).data
        expected_keys = {
            'id', 'entry_detail', 'length', 'refund_times', 'weight', 'count',
            'unit', 'status', 'pretty_status',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class AuxiliaryMaterialInventoryDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inventory_detail = mommy.prepare(
            'AuxiliaryMaterialInventoryDetail',
            entry_detail__unit='unit',
        )

    def test_inventory_detail_fields(self):
        cls = in_detail_serializers.AuxiliaryMaterialInventoryDetailSerializer
        data = cls(self.inventory_detail).data
        expected_keys = {
            'id', 'entry_detail', 'weight', 'count',
            'unit', 'status', 'pretty_status',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentInventoryDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inventory_detail = mommy.prepare(
            'BoughtInComponentInventoryDetail',
            entry_detail__unit='unit',
        )

    def test_inventory_detail_fields(self):
        cls = in_detail_serializers.BoughtInComponentInventoryDetailSerializer
        data = cls(self.inventory_detail).data
        expected_keys = {
            'id', 'entry_detail', 'weight', 'count',
            'unit', 'status', 'pretty_status',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class WeldingMaterialInventoryLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            ('entry_detail__procurement_material'
             '__process_material__material__uid'): 'uid',
        }
        cls.inventory_detail = mommy.prepare(
            'WeldingMaterialInventoryDetail',
            **kwargs,
        )

    def test_inventory_ledger_fields(self):
        data = in_ledger_serializers.WeldingMaterialInventoryLedgerSerializer(
            self.inventory_detail).data
        expected_keys = {
            'id', 'material_mark', 'specification', 'entry_count',
            'entry_dt', 'material_number', 'factory', 'count',
            'pretty_status',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class SteelMaterialInventoryLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            ('entry_detail__procurement_material'
             '__process_material__material__uid'): 'uid',
            ('entry_detail__entry__bidding_sheet'
             '__purchase_order__work_order__uid'): 'uid',
            'warehouse__location': 'location',
        }
        cls.inventory_detail = mommy.prepare(
            'SteelMaterialInventoryDetail',
            **kwargs,
        )

    def test_inventory_ledger_fields(self):
        data = in_ledger_serializers.SteelMaterialInventoryLedgerSerializer(
            self.inventory_detail).data
        expected_keys = {
            'id', 'material', 'batch_number', 'specification',
            'entry_dt', 'material_number', 'work_order_uid',
            'location', 'refund_times', 'count',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class AuxiliaryMaterialInventoryLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            ('entry_detail__procurement_material'
             '__process_material__spec'): 'spec',
        }
        cls.inventory_detail = mommy.prepare(
            'AuxiliaryMaterialInventoryDetail',
            **kwargs,
        )

    def test_inventory_ledger_fields(self):
        cls = in_ledger_serializers.AuxiliaryMaterialInventoryLedgerSerializer
        data = cls(self.inventory_detail).data
        expected_keys = {
            'id', 'specification', 'entry_count', 'entry_dt', 'entry_uid',
            'factory', 'supplier', 'count',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentInventoryLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            ('entry_detail__entry__bidding_sheet'
             '__purchase_order__work_order__uid'): 'uid',
            ('entry_detail__procurement_material'
             '__process_material__material__uid'): 'uid',
        }
        cls.inventory_detail = mommy.prepare(
            'BoughtInComponentInventoryDetail',
            **kwargs,
        )

    def test_inventory_ledger_fields(self):
        cls = in_ledger_serializers.BoughtInComponentInventoryLedgerSerializer
        data = cls(self.inventory_detail).data
        expected_keys = {
            'id', 'work_order_uid', 'specification', 'material',
            'entry_dt', 'material_number', 'entry_uid', 'category', 'count',
        }
        self.assertEqual(set(data.keys()), expected_keys)
