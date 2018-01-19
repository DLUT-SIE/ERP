from unittest.mock import patch, Mock, MagicMock

from django.test import TestCase
from django.utils.timezone import now
from rest_framework import serializers
from model_mommy import mommy

from Inventory import APPLYCARD_STATUS_END, APPLYCARD_STATUS_KEEPER

import Inventory.serializers.entry as entry_serializers
import Inventory.serializers.entry_detail as entry_detail_serializers
import Inventory.serializers.entry_ledger as entry_ledger_serializers
import Inventory.serializers.inventory_detail as in_detail_serializers
import Inventory.serializers.inventory_ledger as in_ledger_serializers
import Inventory.serializers.apply as apply_serializers
import Inventory.serializers.apply_detail as apply_detail_serializers
import Inventory.serializers.apply_ledger as apply_ledger_serializers
import Inventory.serializers.refund as refund_serializers
import Inventory.serializers.refund_detail as re_detail_serializers
import Inventory.serializers.other as other_serializers


class WeldingMaterialEntrySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry = mommy.prepare('WeldingMaterialEntry')

    @patch('Inventory.serializers.entry.WeldingMaterialEntrySerializer'
           '.get_actions')
    def test_welding_material_entry_serializer_fields(self,
                                                      mocked_get_actions):
        data = entry_serializers.WeldingMaterialEntrySerializer(
            self.entry).data
        expected_keys = {'id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                         'purchaser', 'inspector', 'keeper', 'status',
                         'pretty_status', 'details', 'actions'}
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Inventory.serializers.entry.WeldingMaterialEntryListSerializer'
           '.get_actions')
    def test_welding_material_entry_list_serializer_fields(self,
                                                           mocked_get_actions):
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
            'unit', 'factory', 'remark', 'production_dt', 'batch_number',
            'material_number',
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
            'unit', 'factory', 'remark', 'length', 'batch_number',
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
            'unit', 'factory', 'remark', 'batch_number',
        }
        self.assertEqual(set(data.keys()), expected_keys)


class WeldingMaterialEntryLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entry_detail = mommy.prepare(
            'WeldingMaterialEntryDetail',
            procurement_material__process_material__material__uid=123)

    def test_ledger_serializer_fields(self):
        data = entry_ledger_serializers.WeldingMaterialEntryLedgerSerializer(
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
        data = entry_ledger_serializers.SteelMaterialEntryLedgerSerializer(
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
        data = entry_ledger_serializers.AuxiliaryMaterialEntryLedgerSerializer(
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
        data = entry_ledger_serializers.BoughtInComponentEntryLedgerSerializer(
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


class WeldingMaterialApplyCardSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.apply_card = mommy.prepare('WeldingMaterialApplyCard')

    @patch('Inventory.serializers.apply.WeldingMaterialApplyCardSerializer'
           '.get_actions')
    def test_fields(self, mocked_get_actions):
        cls = apply_serializers.WeldingMaterialApplyCardSerializer
        data = cls(self.apply_card).data
        expected_keys = {
            'id', 'department', 'create_dt', 'uid', 'sub_order_uid',
            'welding_seam_uid', 'material_mark', 'model',
            'specification', 'apply_weight', 'apply_count',
            'material_code', 'actual_weight', 'actual_count',
            'applicant', 'auditor', 'inspector', 'keeper',
            'status', 'pretty_status', 'actions'}
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Inventory.serializers.apply.WeldingMaterialApplyCardListSerializer'
           '.get_actions')
    def test_list_fields(self, mocked_get_actions):
        cls = apply_serializers.WeldingMaterialApplyCardListSerializer
        data = cls(self.apply_card).data
        expected_keys = {
            'id', 'sub_order_uid', 'welding_seam_uid', 'material_mark',
            'model', 'specification', 'department', 'create_dt',
            'uid', 'status', 'pretty_status'}
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Process.models.ProcessMaterial.objects.filter')
    def test_create_validate_process_materials(self, mocked_filter):
        cls = apply_serializers.WeldingMaterialApplyCardCreateSerializer
        serializer = cls()

        material_ids = []
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_process_materials(material_ids)

        material_ids = [1, 2, 3]
        mocked_queryset = Mock()
        mocked_filter.return_value = mocked_queryset
        mocked_queryset.count.return_value = 2
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_process_materials(material_ids)

        mocked_queryset.count.return_value = 3
        self.assertIs(serializer.validate_process_materials(material_ids),
                      mocked_queryset)

    @patch('Core.models.SubWorkOrder.objects.filter')
    def test_create_validate_sub_order(self, mocked_filter):
        cls = apply_serializers.WeldingMaterialApplyCardCreateSerializer
        serializer = cls()

        sub_order_id = 1
        mocked_queryset = Mock()
        mocked_filter.return_value = []
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_sub_order(sub_order_id)

        mocked_filter.return_value = [mocked_queryset]
        self.assertIs(serializer.validate_sub_order(sub_order_id),
                      mocked_queryset)

    @patch('Inventory.models.WeldingMaterialApplyCard.create_apply_cards')
    def test_create(self, mocked_create_apply_cards):
        cls = apply_serializers.WeldingMaterialApplyCardCreateSerializer
        serializer = cls()
        serializer.create({})
        mocked_create_apply_cards.assert_called()


class SteelMaterialApplyCardSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.apply_card = mommy.prepare('SteelMaterialApplyCard')

    @patch('Inventory.serializers.apply.SteelMaterialApplyCardSerializer'
           '.get_actions')
    def test_fields(self, mocked_get_actions):
        cls = apply_serializers.SteelMaterialApplyCardSerializer
        data = cls(self.apply_card).data
        expected_keys = {
            'id', 'department', 'create_dt', 'uid', 'applicant',
            'auditor', 'inspector', 'keeper', 'details', 'status',
            'actions'}
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Inventory.serializers.apply.SteelMaterialApplyCardListSerializer'
           '.get_actions')
    def test_list_fields(self, mocked_get_actions):
        cls = apply_serializers.SteelMaterialApplyCardListSerializer
        data = cls(self.apply_card).data
        expected_keys = {
            'id', 'create_dt', 'uid', 'applicant', 'department',
            'status', 'pretty_status'}
        self.assertEqual(set(data.keys()), expected_keys)


class AuxiliaryMaterialApplyCardSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.apply_card = mommy.prepare('AuxiliaryMaterialApplyCard')

    @patch('Inventory.serializers.apply.AuxiliaryMaterialApplyCardSerializer'
           '.get_actions')
    def test_fields(self, mocked_get_actions):
        cls = apply_serializers.AuxiliaryMaterialApplyCardSerializer
        data = cls(self.apply_card).data
        expected_keys = {
            'id', 'sub_order_uid', 'department', 'uid', 'create_dt',
            'applicant', 'auditor', 'inspector', 'keeper',
            'status', 'pretty_status', 'apply_inventory',
            'apply_inventory_name', 'apply_count',
            'actual_inventory_name', 'actual_inventory',
            'actual_count', 'remark', 'actions'}
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Inventory.serializers.apply'
           '.AuxiliaryMaterialApplyCardListSerializer.get_actions')
    def test_list_fields(self, mocked_get_actions):
        cls = apply_serializers.AuxiliaryMaterialApplyCardListSerializer
        data = cls(self.apply_card).data
        expected_keys = {
            'id', 'sub_order_uid', 'uid', 'create_dt',
            'apply_inventory_name', 'apply_count', 'applicant',
            'department', 'status', 'pretty_status'}
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentApplyCardSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.apply_card = mommy.prepare('BoughtInComponentApplyCard')

    @patch('Inventory.serializers.apply.BoughtInComponentApplyCardSerializer'
           '.get_actions')
    def test_fields(self, mocked_get_actions):
        cls = apply_serializers.BoughtInComponentApplyCardSerializer
        data = cls(self.apply_card).data
        expected_keys = {
            'id', 'revised_number', 'sample_report', 'sub_order_uid',
            'department', 'create_dt', 'uid', 'applicant', 'auditor',
            'inspector', 'keeper', 'status', 'pretty_status', 'details',
            'actions'}
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Inventory.serializers.apply'
           '.BoughtInComponentApplyCardListSerializer.get_actions')
    def test_list_fields(self, mocked_get_actions):
        cls = apply_serializers.BoughtInComponentApplyCardListSerializer
        data = cls(self.apply_card).data
        expected_keys = {
            'id', 'sub_order_uid', 'uid', 'create_dt', 'applicant',
            'department', 'status', 'pretty_status'}
        self.assertEqual(set(data.keys()), expected_keys)


class SteelMaterialApplyDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.apply_detail = mommy.prepare('SteelMaterialApplyDetail')

    def test_fields(self):
        cls = apply_detail_serializers.SteelMaterialApplyDetailSerializer
        data = cls(self.apply_detail).data
        expected_keys = {
            'id', 'sub_order_uid', 'material_mark', 'material_code',
            'specification', 'count', 'component'}
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentApplyDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.apply_detail = mommy.prepare('BoughtInComponentApplyDetail')

    def test_fields(self):
        cls = apply_detail_serializers.BoughtInComponentApplyDetailSerializer
        data = cls(self.apply_detail).data
        expected_keys = {
            'id', 'drawing_number', 'specification', 'name', 'count',
            'material_number', 'remark'}
        self.assertEqual(set(data.keys()), expected_keys)


class WeldingMaterialApplyLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.apply_card = mommy.prepare(
            'WeldingMaterialApplyCard',
            applicant__first_name='name')

    def test_ledger_serializer_fields(self):
        data = apply_ledger_serializers.WeldingMaterialApplyLedgerSerializer(
            self.apply_card).data
        expected_keys = {
            'id', 'sub_order_uid', 'welding_seam_uid', 'apply_dt',
            'applicant', 'department', 'apply_card_uid', 'actual_weight',
            'actual_count'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class SteelMaterialApplyLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.apply_detail = mommy.prepare(
            'SteelMaterialApplyDetail',
            process_material__material__name='name')

    def test_ledger_serializer_fields(self):
        data = apply_ledger_serializers.SteelMaterialApplyLedgerSerializer(
            self.apply_detail).data
        expected_keys = {
            'id', 'sub_order_uid', 'material', 'specification',
            'apply_dt', 'material_number', 'apply_count'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class AuxiliaryMaterialApplyLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        kwargs = {
            ('apply_inventory__entry_detail'
             '__procurement_material__process_material__name'): 'name',
            ('actual_inventory__entry_detail'
             '__procurement_material__process_material__spec'): 'spec',
        }
        cls.apply_card = mommy.prepare(
            'AuxiliaryMaterialApplyCard', **kwargs)

    def test_ledger_serializer_fields(self):
        data = apply_ledger_serializers.AuxiliaryMaterialApplyLedgerSerializer(
            self.apply_card).data
        expected_keys = {
            'id', 'department', 'apply_name', 'apply_specification',
            'apply_count', 'apply_card_uid', 'apply_dt',
            'actual_specification', 'actual_count'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentApplyLedgerSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.apply_detail = mommy.prepare(
            'BoughtInComponentApplyDetail',
            process_material__material__name='name')

    def test_ledger_serializer_fields(self):
        data = apply_ledger_serializers.BoughtInComponentApplyLedgerSerializer(
            self.apply_detail).data
        expected_keys = {
            'id', 'sub_order_uid', 'specification', 'material',
            'apply_dt', 'material_number', 'apply_card_uid',
            'apply_count'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class WeldingMaterialRefundCardSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.refund_card = mommy.prepare(
            'WeldingMaterialRefundCard',
            apply_card__process_material__spec='spec')

    @patch('Inventory.serializers.refund'
           '.WeldingMaterialRefundCardSerializer.get_actions')
    def test_fields(self, mocked_get_actions):
        cls = refund_serializers.WeldingMaterialRefundCardSerializer
        data = cls(self.refund_card).data
        expected_keys = {
            'id', 'department', 'create_dt', 'uid', 'sub_order_uid',
            'apply_card_create_dt', 'apply_card_uid', 'model',
            'specification', 'weight', 'count', 'refunder', 'keeper',
            'status', 'pretty_status', 'actions'
        }
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Inventory.serializers.refund'
           '.WeldingMaterialRefundCardListSerializer.get_actions')
    def test_list_fields(self, mocked_get_actions):
        cls = refund_serializers.WeldingMaterialRefundCardListSerializer
        data = cls(self.refund_card).data
        expected_keys = {
            'id', 'sub_order_uid', 'department', 'create_dt', 'uid',
            'welding_seam_uid', 'status', 'pretty_status',
        }
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Inventory.models.apply.WeldingMaterialApplyCard.objects.filter')
    def test_create_validate_details_dict(self, mocked_filter):
        cls = refund_serializers.WeldingMaterialRefundCardCreateSerializer
        serializer = cls()
        details_dict = {'1': 1, '2': 2, '3': 3}
        apply_details = MagicMock()
        mocked_filter.return_value = apply_details

        details = []
        apply_details.__iter__.return_value = details
        apply_details.count.return_value = 0
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_details_dict(details_dict)

        details = [Mock(id=str(i+1)) for i in range(3)]
        apply_details.__iter__.return_value = details
        apply_details.count.return_value = 3
        ret = serializer.validate_details_dict(details_dict)

        mocked_filter.assert_called()
        apply_details.count.assert_called()
        for detail in details:
            self.assertIn(detail, ret)
            self.assertEqual(ret[detail], details_dict[detail.id])

    @patch('Inventory.models.apply.WeldingMaterialApplyCard.objects.filter')
    def test_create_validate_apply_Card(self, mocked_filter):
        cls = refund_serializers.WeldingMaterialRefundCardCreateSerializer
        serializer = cls()
        apply_card_id = 1

        mocked_filter.return_value = []
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_apply_card(apply_card_id)

        apply_card = Mock()
        apply_card.status = APPLYCARD_STATUS_KEEPER
        mocked_filter.return_value = [apply_card]
        with self.assertRaises(serializers.ValidationError):
            serializer.validate_apply_card(apply_card_id)

        apply_card.status = APPLYCARD_STATUS_END
        ret = serializer.validate_apply_card(apply_card_id)
        mocked_filter.assert_called()
        self.assertEqual(ret, apply_card)

    def test_create_validate(self):
        cls = refund_serializers.WeldingMaterialRefundCardCreateSerializer
        serializer = cls()
        # TODO: 待序列化器更新后更新测试用例
        self.assertEqual(serializer.validate({}), {})

    @patch('Inventory.models.refund.WeldingMaterialRefundCard'
           '.create_refund_cards')
    def test_create(self, mocked_create_refund_cards):
        cls = refund_serializers.WeldingMaterialRefundCardCreateSerializer
        serializer = cls()
        serializer.create({})
        mocked_create_refund_cards.assert_called()


class SteelMaterialRefundCardSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.refund_card = mommy.prepare(
            'SteelMaterialRefundCard',
            apply_card__sub_order__id=1)

    @patch('Inventory.serializers.refund'
           '.SteelMaterialRefundCardSerializer.get_actions')
    def test_fields(self, mocked_get_actions):
        cls = refund_serializers.SteelMaterialRefundCardSerializer
        data = cls(self.refund_card).data
        expected_keys = {
            'id', 'sub_order_uid', 'create_dt', 'uid', 'steel_type',
            'refunder', 'inspector', 'keeper', 'status', 'pretty_status',
            'board_details', 'bar_details', 'actions'
        }
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Inventory.serializers.refund'
           '.SteelMaterialRefundCardListSerializer.get_actions')
    def test_list_fields(self, mocked_get_actions):
        cls = refund_serializers.SteelMaterialRefundCardListSerializer
        data = cls(self.refund_card).data
        expected_keys = {
            'id', 'create_dt', 'uid', 'sub_order_uid', 'steel_type',
            'refunder', 'status', 'pretty_status'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentRefundCardSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.refund_card = mommy.prepare(
            'BoughtInComponentRefundCard',
            apply_card__sub_order__id=1)

    @patch('Inventory.serializers.refund'
           '.BoughtInComponentRefundCardSerializer.get_actions')
    def test_fields(self, mocked_get_actions):
        cls = refund_serializers.BoughtInComponentRefundCardSerializer
        data = cls(self.refund_card).data
        expected_keys = {
            'id', 'sub_order_uid', 'department', 'uid', 'refunder',
            'keeper', 'status', 'pretty_status', 'details', 'actions'
        }
        self.assertEqual(set(data.keys()), expected_keys)

    @patch('Inventory.serializers.refund'
           '.BoughtInComponentRefundCardListSerializer.get_actions')
    def test_list_fields(self, mocked_get_actions):
        cls = refund_serializers.BoughtInComponentRefundCardListSerializer
        data = cls(self.refund_card).data
        expected_keys = {
            'id', 'uid', 'create_dt', 'refunder', 'status', 'pretty_status'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class BoardSteelMaterialRefundDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.refund_detail = mommy.prepare(
            'BoardSteelMaterialRefundDetail',
            apply_detail__process_material__material__id=1,
            refund_card__apply_card__uid='uid')

    def test_fields(self):
        cls = re_detail_serializers.BoardSteelMaterialRefundDetailSerializer
        data = cls(self.refund_detail).data
        expected_keys = {
            'id', 'name', 'material', 'specification', 'material_code',
            'status', 'count', 'weight', 'apply_card_uid'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class BarSteelMaterialRefundDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.refund_detail = mommy.prepare(
            'BarSteelMaterialRefundDetail',
            apply_detail__process_material__material__id=1,
            refund_card__apply_card__uid='uid')

    def test_fields(self):
        cls = re_detail_serializers.BarSteelMaterialRefundDetailSerializer
        data = cls(self.refund_detail).data
        expected_keys = {
            'id', 'name', 'material', 'specification', 'material_code',
            'status', 'count', 'weight', 'apply_card_uid'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class BoughtInComponentRefundDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.refund_detail = mommy.prepare(
            'BoughtInComponentRefundDetail',
            apply_detail__process_material__drawing_number='number',
            apply_detail__inventory_detail__entry_detail__unit='unit')

    def test_fields(self):
        cls = re_detail_serializers.BoughtInComponentRefundDetailSerializer
        data = cls(self.refund_detail).data
        expected_keys = {
            'id', 'drawing_number', 'specification', 'name', 'unit',
            'count', 'material_number', 'remark'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class WarehouseSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.warehourse = mommy.prepare('Warehouse')

    def test_fields(self):
        cls = other_serializers.WarehouseSerializer
        data = cls(self.warehourse).data
        expected_keys = {
            'id', 'name', 'location', 'category', 'pretty_category'
        }
        self.assertEqual(set(data.keys()), expected_keys)


class WeldingMaterialHumitureRecordSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.warehourse = mommy.prepare('WeldingMaterialHumitureRecord')

    def test_fields(self):
        cls = other_serializers.WeldingMaterialHumitureRecordSerializer
        data = cls(self.warehourse).data
        expected_keys = {
            'id', 'create_dt', 'keeper', 'actual_temp_1',
            'actual_humid_1', 'actual_temp_2', 'actual_humid_2',
            'remark'
        }
        self.assertEqual(set(data.keys()), expected_keys)

    def test_list_fields(self):
        cls = other_serializers.WeldingMaterialHumitureRecordListSerializer
        data = cls(self.warehourse).data
        expected_keys = {'id', 'create_dt', 'keeper'}
        self.assertEqual(set(data.keys()), expected_keys)


class WeldingMaterialBakeRecordSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.warehourse = mommy.prepare('WeldingMaterialBakeRecord')

    def test_fields(self):
        cls = other_serializers.WeldingMaterialBakeRecordSerializer
        data = cls(self.warehourse).data
        expected_keys = {
            'id', 'create_dt', 'standard_num', 'size', 'class_num',
            'heat_num', 'codedmark', 'quantity', 'furnace_time',
            'baking_temp', 'heating_time', 'cooling_time',
            'holding_time', 'holding_temp', 'apply_time', 'keeper',
            'welding_engineer', 'remark'
        }
        self.assertEqual(set(data.keys()), expected_keys)

    def test_list_fields(self):
        cls = other_serializers.WeldingMaterialBakeRecordListSerializer
        data = cls(self.warehourse).data
        expected_keys = {
            'id', 'create_dt', 'standard_num', 'size', 'heat_num',
            'codedmark', 'keeper', 'welding_engineer'
        }
        self.assertEqual(set(data.keys()), expected_keys)
