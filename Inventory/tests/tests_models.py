from unittest.mock import Mock, patch

from django.test import TestCase
from django.core import exceptions
from django.utils.timezone import now
from model_mommy import mommy

from Inventory import (
    ENTRYSTATUS_CHOICES_INSPECTOR, ENTRYSTATUS_CHOICES_KEEPER,
    ENTRYSTATUS_CHOICES_END,
    APPLYCARD_STATUS_AUDITOR, APPLYCARD_STATUS_INSPECTOR,
    APPLYCARD_STATUS_KEEPER, APPLYCARD_STATUS_END,
    REFUNDSTATUS_INSPECTOR, REFUNDSTATUS_KEEPER, REFUNDSTATUS_END,
    STEEL_TYPE_BOARD_STEEL, STEEL_TYPE_BAR_STEEL,
)


class WeldingMaterialEntryTest(TestCase):
    def setUp(self):
        self.entry = mommy.prepare('WeldingMaterialEntry')

    def test_str(self):
        entry = self.entry
        expected_str = entry.uid
        self.assertEqual(str(entry), expected_str)

    def test_purchaser_confirm(self):
        entry = self.entry
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        entry.purchaser_confirm(request)
        self.assertIs(entry.purchaser, user)
        self.assertIs(entry.status, ENTRYSTATUS_CHOICES_INSPECTOR)

    def test_inspector_confirm(self):
        entry = self.entry
        entry.status = ENTRYSTATUS_CHOICES_INSPECTOR
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        entry.inspector_confirm(request)
        self.assertIs(entry.inspector, user)
        self.assertIs(entry.status, ENTRYSTATUS_CHOICES_KEEPER)

    @patch('Inventory.models.entry.WeldingMaterialInventoryDetail')
    @patch('Inventory.models.entry.WeldingMaterialEntry.details')
    def test_keeper_confirm(self, mocked_details, mocked_inventory_detail_cls):
        entry = self.entry
        entry.status = ENTRYSTATUS_CHOICES_KEEPER
        mocked_details.all.return_value = mommy.prepare(
            'WeldingMaterialEntryDetail', _quantity=3, production_dt=now())
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        entry.keeper_confirm(request)
        self.assertIs(entry.keeper, user)
        self.assertIs(entry.status, ENTRYSTATUS_CHOICES_END)
        mocked_inventory_detail_cls.objects.bulk_create.assert_called()

    @patch('Inventory.models.entry.WeldingMaterialEntry.save')
    @patch('Inventory.models.entry_detail.WeldingMaterialEntryDetail'
           '.objects.bulk_create')
    @patch('Procurement.models.other.ArrivalInspection'
           '.entry_confirm')
    def test_create_entry(self, mocked_confirm, mocked_bulk_create,
                          mocked_save):
        entry = self.entry
        acceptance = mommy.prepare('BiddingAcceptance')
        acceptance.accept_supplier = mommy.prepare('Supplier')
        inspections = mommy.prepare('ArrivalInspection', _quantity=3)
        bidding_sheet = acceptance.bidding_sheet
        entry.create_entry(bidding_sheet, inspections)
        mocked_save.assert_called()
        mocked_bulk_create.assert_called()
        self.assertEqual(mocked_confirm.call_count, 3)


class SteelMaterialEntryTest(TestCase):
    def setUp(self):
        self.entry = mommy.prepare('SteelMaterialEntry')

    @patch('Inventory.models.entry.SteelMaterialInventoryDetail')
    @patch('Inventory.models.entry.SteelMaterialEntry.details')
    def test_keeper_confirm(self, mocked_details, mocked_inventory_detail_cls):
        entry = self.entry
        entry.status = ENTRYSTATUS_CHOICES_KEEPER
        mocked_details.all.return_value = mommy.prepare(
            'SteelMaterialEntryDetail', _quantity=3)
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        entry.keeper_confirm(request)
        self.assertIs(entry.keeper, user)
        self.assertIs(entry.status, ENTRYSTATUS_CHOICES_END)
        mocked_inventory_detail_cls.objects.bulk_create.assert_called()


class AuxiliaryMaterialEntryTest(TestCase):
    def setUp(self):
        self.entry = mommy.prepare('AuxiliaryMaterialEntry')

    @patch('Inventory.models.entry.AuxiliaryMaterialEntry'
           '.create_inventory_details')
    def test_keeper_confirm(self, mocked_create_details):
        entry = self.entry
        entry.status = ENTRYSTATUS_CHOICES_KEEPER
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        entry.keeper_confirm(request)
        self.assertIs(entry.keeper, user)
        self.assertIs(entry.status, ENTRYSTATUS_CHOICES_END)
        mocked_create_details.assert_called()


class BoughtInComponentEntryTest(TestCase):
    def setUp(self):
        self.entry = mommy.prepare('BoughtInComponentEntry')

    @patch('Inventory.models.entry.BoughtInComponentEntry'
           '.create_inventory_details')
    def test_keeper_confirm(self, mocked_create_details):
        entry = self.entry
        entry.status = ENTRYSTATUS_CHOICES_KEEPER
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        entry.keeper_confirm(request)
        self.assertIs(entry.keeper, user)
        self.assertIs(entry.status, ENTRYSTATUS_CHOICES_END)
        mocked_create_details.assert_called()


class WeldingMaterialEntryDetailTest(TestCase):
    def setUp(self):
        self.detail = mommy.make('WeldingMaterialEntryDetail')

    def test_str(self):
        detail = self.detail
        expected_str = '{}-{}'.format(detail.entry,
                                      detail.procurement_material)
        self.assertEqual(str(detail), expected_str)


class WeldingMaterialInventoryDetailTest(TestCase):
    def setUp(self):
        self.detail = mommy.make('WeldingMaterialInventoryDetail')

    def test_str(self):
        detail = self.detail
        expected_str = str(detail.entry_detail)
        self.assertEqual(str(detail), expected_str)


class WeldingMaterialApplyCardTest(TestCase):
    def setUp(self):
        self.apply_card = mommy.prepare('WeldingMaterialApplyCard')

    def test_str(self):
        apply_card = self.apply_card
        expected_str = apply_card.uid
        self.assertEqual(str(apply_card), expected_str)

    @patch('Inventory.models.apply.WeldingMaterialApplyCard.objects.last')
    def test_gen_uid_index(self, mocked_last):
        apply_card = self.apply_card
        mocked_last.return_value = None
        index = apply_card.gen_uid_index()
        self.assertEqual(index, 1)
        mock_id = Mock()
        mock_id.id = 2
        mocked_last.return_value = mock_id
        index = apply_card.gen_uid_index()
        self.assertEqual(index, 3)

    def test_applicant_confirm(self):
        apply_card = self.apply_card
        request = Mock()
        user = mommy.prepare('User')
        request.user = user

        with self.assertRaises(exceptions.ValidationError):
            apply_card.applicant_confirm(request)

        apply_card.apply_weight = 1
        apply_card.apply_count = 1
        apply_card.applicant_confirm(request)
        self.assertIs(apply_card.applicant, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_AUDITOR)

    def test_auditor_confirm(self):
        apply_card = self.apply_card
        apply_card.status = APPLYCARD_STATUS_AUDITOR
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        apply_card.auditor_confirm(request)
        self.assertIs(apply_card.auditor, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_INSPECTOR)

    def test_inspector_confirm(self):
        apply_card = self.apply_card
        apply_card.status = APPLYCARD_STATUS_INSPECTOR
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        apply_card.inspector_confirm(request)
        self.assertIs(apply_card.inspector, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_KEEPER)

    @patch('Inventory.models.inventory_detail.WeldingMaterialInventoryDetail'
           '.save')
    def test_keeper_confirm(self, mocked_save):
        apply_card = self.apply_card
        apply_card.status = APPLYCARD_STATUS_KEEPER
        request = Mock()
        user = mommy.prepare('User')
        request.user = user

        with self.assertRaises(exceptions.ValidationError):
            apply_card.keeper_confirm(request)

        apply_card.actual_weight = 1
        apply_card.actual_count = 1

        inventory_detail = mommy.prepare('WeldingMaterialInventoryDetail',
                                         count=0)
        apply_card.inventory = inventory_detail
        with self.assertRaises(exceptions.ValidationError):
            apply_card.keeper_confirm(request)

        inventory_detail = mommy.prepare('WeldingMaterialInventoryDetail',
                                         count=2)
        apply_card.inventory = inventory_detail
        apply_card.keeper_confirm(request)
        self.assertIs(apply_card.keeper, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_END)
        self.assertEqual(inventory_detail.count, 1)
        mocked_save.assert_called()

    @patch('Inventory.models.apply.WeldingMaterialApplyCard'
           '.objects.bulk_create')
    def test_create_apply_cards(self, mocked_bulk_create):
        apply_card = self.apply_card
        sub_order = mommy.prepare('SubWorkOrder')
        process_materials = mommy.prepare('ProcessMaterial', _quantity=3)
        apply_card.create_apply_cards(sub_order, process_materials)
        mocked_bulk_create.assert_called()


class SteelMaterialApplyCardTest(TestCase):
    def setUp(self):
        self.apply_card = mommy.prepare('SteelMaterialApplyCard')

    @patch('Inventory.models.apply.SteelMaterialApplyCard.details')
    def test_applicant_confirm(self, mocked_details):
        apply_card = self.apply_card
        mocked_details.all.return_value = mommy.prepare(
            'SteelMaterialApplyDetail', _quantity=3)
        request = Mock()
        user = mommy.prepare('User')
        request.user = user

        with self.assertRaises(exceptions.ValidationError):
            apply_card.applicant_confirm(request)

        mocked_details.all.return_value = mommy.prepare(
            'SteelMaterialApplyDetail', _quantity=3, count=2)

        apply_card.applicant_confirm(request)
        self.assertIs(apply_card.applicant, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_AUDITOR)

    @patch('Inventory.models.inventory_detail.SteelMaterialInventoryDetail'
           '.save')
    @patch('Inventory.models.apply.SteelMaterialApplyCard.details')
    def test_keeper_confirm(self, mocked_details, mocked_save):
        apply_card = self.apply_card
        apply_card.status = APPLYCARD_STATUS_KEEPER
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        mocked_details.all.return_value = mocked_details

        details = mommy.prepare('SteelMaterialApplyDetail', _quantity=3)
        mocked_details.select_related.return_value = details
        with self.assertRaises(exceptions.ValidationError):
            apply_card.keeper_confirm(request)

        details = mommy.prepare('SteelMaterialApplyDetail', _quantity=3,
                                inventory_detail__count=2, count=3)
        mocked_details.select_related.return_value = details
        with self.assertRaises(exceptions.ValidationError):
            apply_card.keeper_confirm(request)

        details = mommy.prepare('SteelMaterialApplyDetail', _quantity=3,
                                inventory_detail__count=3, count=1)
        mocked_details.select_related.return_value = details
        apply_card.keeper_confirm(request)

        self.assertIs(apply_card.keeper, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_END)
        for detail in details:
            self.assertEqual(detail.inventory_detail.count, 2)
        self.assertEqual(mocked_save.call_count, 3)

    @patch('Inventory.models.apply_detail.SteelMaterialApplyDetail'
           '.objects.bulk_create')
    @patch('Inventory.models.apply.SteelMaterialApplyCard.objects')
    def test_create_apply_cards(self, mocked_objects, mocked_bulk_create):
        apply_card = self.apply_card
        mocked_objects.create.return_value = mommy.prepare(
            'SteelMaterialApplyCard')
        sub_order = mommy.prepare('SubWorkOrder')
        process_materials = mommy.prepare('ProcessMaterial', _quantity=3)
        apply_card.create_apply_cards(sub_order, process_materials)
        mocked_bulk_create.assert_called()


class AuxiliaryMaterialApplyCardTest(TestCase):
    def setUp(self):
        self.apply_card = mommy.prepare('AuxiliaryMaterialApplyCard')

    def test_applicant_confirm(self):
        apply_card = self.apply_card
        request = Mock()
        user = mommy.prepare('User')
        request.user = user

        with self.assertRaises(exceptions.ValidationError):
            apply_card.applicant_confirm(request)

        apply_card.apply_inventory = mommy.prepare(
            'AuxiliaryMaterialInventoryDetail')
        apply_card.apply_count = 1
        apply_card.applicant_confirm(request)
        self.assertIs(apply_card.applicant, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_AUDITOR)

    @patch('Inventory.models.inventory_detail.AuxiliaryMaterialInventoryDetail'
           '.save')
    def test_keeper_confirm(self, mocked_save):
        apply_card = self.apply_card
        apply_card.status = APPLYCARD_STATUS_KEEPER
        request = Mock()
        user = mommy.prepare('User')
        request.user = user

        with self.assertRaises(exceptions.ValidationError):
            apply_card.keeper_confirm(request)

        inventory_detail = mommy.prepare('AuxiliaryMaterialInventoryDetail',
                                         count=0)
        apply_card.actual_inventory = inventory_detail
        apply_card.actual_count = 1
        with self.assertRaises(exceptions.ValidationError):
            apply_card.keeper_confirm(request)

        inventory_detail = mommy.prepare('AuxiliaryMaterialInventoryDetail',
                                         count=2)
        apply_card.actual_inventory = inventory_detail
        apply_card.keeper_confirm(request)
        self.assertIs(apply_card.keeper, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_END)
        self.assertEqual(inventory_detail.count, 1)
        mocked_save.assert_called()

    @patch('Inventory.models.apply.AuxiliaryMaterialApplyCard'
           '.objects.bulk_create')
    def test_create_apply_cards(self, mocked_bulk_create):
        apply_card = self.apply_card
        sub_order = mommy.prepare('SubWorkOrder')
        process_materials = mommy.prepare('ProcessMaterial', _quantity=3)
        apply_card.create_apply_cards(sub_order, process_materials)
        mocked_bulk_create.assert_called()


class BoughtInComponentApplyCardTest(TestCase):
    def setUp(self):
        self.apply_card = mommy.prepare('BoughtInComponentApplyCard')

    @patch('Inventory.models.apply.BoughtInComponentApplyCard.details')
    def test_applicant_confirm(self, mocked_details):
        apply_card = self.apply_card
        mocked_details.all.return_value = mommy.prepare(
            'BoughtInComponentApplyDetail', _quantity=3)
        request = Mock()
        user = mommy.prepare('User')
        request.user = user

        with self.assertRaises(exceptions.ValidationError):
            apply_card.applicant_confirm(request)

        mocked_details.all.return_value = mommy.prepare(
            'BoughtInComponentApplyDetail', _quantity=3, count=2)

        apply_card.applicant_confirm(request)
        self.assertIs(apply_card.applicant, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_AUDITOR)

    @patch('Inventory.models.inventory_detail.BoughtInComponentInventoryDetail'
           '.save')
    @patch('Inventory.models.apply.BoughtInComponentApplyCard.details')
    def test_keeper_confirm(self, mocked_details, mocked_save):
        apply_card = self.apply_card
        apply_card.status = APPLYCARD_STATUS_KEEPER
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        mocked_details.all.return_value = mocked_details

        details = mommy.prepare('BoughtInComponentApplyDetail', _quantity=3)
        mocked_details.select_related.return_value = details
        with self.assertRaises(exceptions.ValidationError):
            apply_card.keeper_confirm(request)

        details = mommy.prepare('BoughtInComponentApplyDetail', _quantity=3,
                                inventory_detail__count=2, count=3)
        mocked_details.select_related.return_value = details
        with self.assertRaises(exceptions.ValidationError):
            apply_card.keeper_confirm(request)

        details = mommy.prepare('BoughtInComponentApplyDetail', _quantity=3,
                                inventory_detail__count=3, count=1)
        mocked_details.select_related.return_value = details
        apply_card.keeper_confirm(request)

        self.assertIs(apply_card.keeper, user)
        self.assertIs(apply_card.status, APPLYCARD_STATUS_END)
        for detail in details:
            self.assertEqual(detail.inventory_detail.count, 2)
        self.assertEqual(mocked_save.call_count, 3)

    @patch('Inventory.models.apply_detail.BoughtInComponentApplyDetail'
           '.objects.bulk_create')
    @patch('Inventory.models.apply.BoughtInComponentApplyCard.objects')
    def test_create_apply_cards(self, mocked_objects, mocked_bulk_create):
        apply_card = self.apply_card
        mocked_objects.create.return_value = mommy.prepare(
            'BoughtInComponentApplyCard')
        sub_order = mommy.prepare('SubWorkOrder')
        process_materials = mommy.prepare('ProcessMaterial', _quantity=3)
        apply_card.create_apply_cards(sub_order, process_materials)
        mocked_bulk_create.assert_called()


class SteelMaterialApplyDetailTestCase(TestCase):
    def setUp(self):
        self.detail = mommy.prepare('SteelMaterialApplyDetail')

    def test_str(self):
        detail = self.detail
        expected_str = str(detail.process_material)
        self.assertEqual(str(detail), expected_str)


class WeldingMaterialRefundCardTest(TestCase):
    def setUp(self):
        self.refund_card = mommy.prepare('WeldingMaterialRefundCard')

    def test_str(self):
        refund_card = self.refund_card
        expected_str = str(refund_card.apply_card)
        self.assertEqual(str(refund_card), expected_str)

    @patch('Inventory.models.refund.WeldingMaterialRefundCard.objects.last')
    def test_gen_uid_index(self, mocked_last):
        refund_card = self.refund_card
        mocked_last.return_value = None
        index = refund_card.gen_uid_index()
        self.assertEqual(index, 1)
        mock_id = Mock()
        mock_id.id = 2
        mocked_last.return_value = mock_id
        index = refund_card.gen_uid_index()
        self.assertEqual(index, 3)

    def test_refunder_confirm(self):
        refund_card = self.refund_card
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        with self.assertRaises(exceptions.ValidationError):
            refund_card.refunder_confirm(request)

        refund_card.weight = 1
        refund_card.count = 2
        refund_card.apply_card = mommy.prepare('WeldingMaterialApplyCard',
                                               actual_count=1)
        with self.assertRaises(exceptions.ValidationError):
            refund_card.refunder_confirm(request)

        refund_card.apply_card = mommy.prepare('WeldingMaterialApplyCard',
                                               actual_count=2)
        refund_card.refunder_confirm(request)
        self.assertIs(refund_card.refunder, user)
        self.assertIs(refund_card.status, REFUNDSTATUS_INSPECTOR)

    def test_inspector_confirm(self):
        refund_card = self.refund_card
        refund_card.status = REFUNDSTATUS_INSPECTOR
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        refund_card.inspector_confirm(request)
        self.assertIs(refund_card.inspector, user)
        self.assertIs(refund_card.status, REFUNDSTATUS_KEEPER)

    @patch('Inventory.models.refund.WeldingMaterialRefundCard.apply_card')
    def test_keeper_confirm(self, mocked_apply_card):
        refund_card = self.refund_card
        refund_card.status = REFUNDSTATUS_KEEPER
        refund_card.count = 2
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        inventory = Mock()
        inventory.count = 0
        mocked_apply_card.inventory = inventory
        refund_card.keeper_confirm(request)
        self.assertIs(refund_card.keeper, user)
        self.assertIs(refund_card.status, REFUNDSTATUS_END)
        self.assertEqual(inventory.count, 2)
        inventory.save.assert_called()

    @patch('Inventory.models.refund.WeldingMaterialRefundCard.objects.create')
    def test_create_refund_cards(self, mocked_create):
        refund_card = self.refund_card
        apply_card = Mock()
        refund_card.create_refund_cards(apply_card, {'count': 5})
        mocked_create.assert_called()


class SteelMaterialRefundCardTest(TestCase):
    def setUp(self):
        self.refund_card = mommy.prepare('SteelMaterialRefundCard')

    def test_str(self):
        refund_card = self.refund_card
        expected_str = refund_card.uid
        self.assertEqual(str(refund_card), expected_str)

    @patch('Inventory.models.refund.SteelMaterialRefundCard.board_details')
    @patch('Inventory.models.refund.SteelMaterialRefundCard.bar_details')
    def test_refunder_confirm(self, mocked_bar_details, mocked_board_details):
        refund_card = self.refund_card
        request = Mock()
        user = mommy.prepare('User')
        request.user = user

        board_details = mommy.prepare('BoardSteelMaterialRefundDetail',
                                      _quantity=3, count=5,
                                      apply_detail__count=2)
        bar_details = mommy.prepare('BarSteelMaterialRefundDetail',
                                    _quantity=2)
        mocked_bar_details.select_related.return_value = bar_details
        mocked_board_details.select_related.return_value = board_details
        with self.assertRaises(exceptions.ValidationError):
            refund_card.refunder_confirm(request)

        board_details = mommy.prepare('BoardSteelMaterialRefundDetail',
                                      _quantity=3, count=5,
                                      apply_detail__count=5)
        bar_details = mommy.prepare('BarSteelMaterialRefundDetail',
                                    _quantity=2, count=5,
                                    apply_detail__count=2)
        mocked_bar_details.select_related.return_value = bar_details
        mocked_board_details.select_related.return_value = board_details
        with self.assertRaises(exceptions.ValidationError):
            refund_card.refunder_confirm(request)

        board_details = mommy.prepare('BoardSteelMaterialRefundDetail',
                                      _quantity=3, count=5,
                                      apply_detail__count=5)
        bar_details = mommy.prepare('BarSteelMaterialRefundDetail',
                                    _quantity=2, count=5,
                                    apply_detail__count=5,
                                    length=1,
                                    apply_detail__inventory_detail__length=5)
        mocked_bar_details.select_related.return_value = bar_details
        mocked_board_details.select_related.return_value = board_details
        refund_card.refunder_confirm(request)

    @patch('Inventory.models.refund.SteelMaterialInventoryDetail'
           '.objects.create')
    @patch('Inventory.models.refund.SteelMaterialRefundCard.board_details')
    @patch('Inventory.models.refund.SteelMaterialRefundCard.bar_details')
    def test_keeper_confirm(self, mocked_board_details, mocked_bar_details,
                            mocked_create):
        refund_card = self.refund_card
        refund_card.status = REFUNDSTATUS_KEEPER
        request = Mock()
        user = mommy.prepare('User')
        request.user = user

        board_details = mommy.prepare(
            'BoardSteelMaterialRefundDetail', _quantity=3,
            apply_detail__inventory_detail__refund_times=0)
        bar_details = mommy.prepare(
            'BarSteelMaterialRefundDetail', _quantity=2,
            apply_detail__inventory_detail__refund_times=0)
        mocked_bar_details.select_related.return_value = bar_details
        mocked_board_details.select_related.return_value = board_details
        refund_card.keeper_confirm(request)

        self.assertIs(refund_card.keeper, user)
        self.assertIs(refund_card.status, REFUNDSTATUS_END)
        self.assertEqual(mocked_create.call_count, 5)

    @patch('Inventory.models.refund_detail.BoardSteelMaterialRefundDetail'
           '.objects.bulk_create')
    @patch('Inventory.models.refund_detail.BarSteelMaterialRefundDetail'
           '.objects.bulk_create')
    @patch('Inventory.models.refund.SteelMaterialRefundCard.objects.create')
    def test_create_refund_cards(self, mocked_create, mocked_bar_bulk_create,
                                 mocked_board_bulk_create):
        refund_card = self.refund_card
        apply_card = Mock()
        mocked_create.return_value = mommy.prepare('SteelMaterialRefundCard')
        bar_kwargs = {
            ('inventory_detail__entry_detail'
             '__entry__steel_type'): STEEL_TYPE_BAR_STEEL
        }
        board_kwargs = {
            ('inventory_detail__entry_detail'
             '__entry__steel_type'): STEEL_TYPE_BOARD_STEEL
        }
        details_dict = {mommy.prepare('SteelMaterialApplyDetail', id=i,
                                      **bar_kwargs): 1 for i in range(3)}
        details_dict.update({
            mommy.prepare('SteelMaterialApplyDetail', id=i+3,
                          **board_kwargs): 1 for i in range(3)})
        refund_card.create_refund_cards(apply_card, details_dict)
        mocked_create.assert_called()
        mocked_bar_bulk_create.assert_called()
        mocked_board_bulk_create.assert_called()


class BoughtInComponentRefundCardTest(TestCase):
    def setUp(self):
        self.refund_card = mommy.prepare('BoughtInComponentRefundCard')

    @patch('Inventory.models.refund.BoughtInComponentRefundCard.details')
    def test_refunder_confirm(self, mocked_details):
        refund_card = self.refund_card
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        mocked_details.select_related.return_value = mommy.prepare(
            'BoughtInComponentRefundDetail',
            count=5,
            apply_detail__count=2,
            _quantity=3)

        with self.assertRaises(exceptions.ValidationError):
            refund_card.refunder_confirm(request)

        mocked_details.select_related.return_value = mommy.prepare(
            'BoughtInComponentRefundDetail',
            count=5,
            apply_detail__count=5,
            _quantity=3)
        refund_card.refunder_confirm(request)
        self.assertEqual(refund_card.refunder, user)
        self.assertEqual(refund_card.status, REFUNDSTATUS_INSPECTOR)

    @patch('Inventory.models.inventory_detail.BoughtInComponentInventoryDetail'
           '.save')
    @patch('Inventory.models.refund.BoughtInComponentRefundCard.details')
    def test_keeper_confirm(self, mocked_details, mocked_save):
        refund_card = self.refund_card
        refund_card.status = REFUNDSTATUS_KEEPER
        refund_card.count = 2
        request = Mock()
        user = mommy.prepare('User')
        request.user = user
        refund_details = mommy.prepare(
            'BoughtInComponentRefundDetail',
            _quantity=3,
            apply_detail__inventory_detail__count=0,
            count=5)
        mocked_details.select_related.return_value = refund_details
        refund_card.keeper_confirm(request)
        self.assertIs(refund_card.keeper, user)
        self.assertIs(refund_card.status, REFUNDSTATUS_END)
        for refund_detail in refund_details:
            self.assertEqual(
                refund_detail.apply_detail.inventory_detail.count, 5)
        self.assertEqual(mocked_save.call_count, 3)

    @patch('Inventory.models.BoughtInComponentRefundDetail'
           '.objects.bulk_create')
    @patch('Inventory.models.refund.BoughtInComponentRefundCard'
           '.objects.create')
    def test_create_refund_cards(self, mocked_create, mocked_bulk_create):
        refund_card = self.refund_card
        apply_card = Mock()
        mocked_create.return_value = mommy.prepare(
            'BoughtInComponentRefundCard')
        details_dict = {mommy.prepare('BoughtInComponentApplyDetail',
                                      id=i): 1 for i in range(3)}
        refund_card.create_refund_cards(apply_card, details_dict)
        mocked_create.assert_called()
        mocked_bulk_create.assert_called()


class BoardSteelMaterialRefundDetailTest(TestCase):
    def setUp(self):
        self.detail = mommy.prepare('BoardSteelMaterialRefundDetail')

    def test_str(self):
        detail = self.detail
        expected_str = str(detail.apply_detail)
        self.assertEqual(str(detail), expected_str)


class BoughtInComponentRefundDetailTest(TestCase):
    def setUp(self):
        self.detail = mommy.prepare('BoughtInComponentRefundDetail')

    def test_str(self):
        detail = self.detail
        expected_str = '{}({})'.format(detail.apply_detail, detail.refund_card)
        self.assertEqual(str(detail), expected_str)


class WarehouseTest(TestCase):
    def setUp(self):
        self.detail = mommy.prepare('Warehouse')

    def test_str(self):
        detail = self.detail
        expected_str = detail.name
        self.assertEqual(str(detail), expected_str)


class WeldingMaterialHumitureRecordTest(TestCase):
    def setUp(self):
        self.detail = mommy.prepare('WeldingMaterialHumitureRecord')

    def test_str(self):
        detail = self.detail
        expected_str = '{}({})'.format(detail.create_dt, detail.keeper)
        self.assertEqual(str(detail), expected_str)


class WeldingMaterialBakeRecordTest(TestCase):
    def setUp(self):
        self.detail = mommy.prepare('WeldingMaterialBakeRecord')

    def test_str(self):
        detail = self.detail
        expected_str = str(detail.create_dt)
        self.assertEqual(str(detail), expected_str)


class WeldingWarehouseThresholdTest(TestCase):
    def setUp(self):
        self.detail = mommy.prepare('WeldingWarehouseThreshold')

    def test_str(self):
        detail = self.detail
        expected_str = detail.specification
        self.assertEqual(str(detail), expected_str)


class InventoryTerminationRecordTest(TestCase):
    def setUp(self):
        self.detail = mommy.prepare('InventoryTerminationRecord')

    def test_str(self):
        detail = self.detail
        expected_str = '{}({})'.format(detail.uid, detail.category)
        self.assertEqual(str(detail), expected_str)
