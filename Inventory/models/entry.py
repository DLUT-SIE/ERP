from django.db import models
from django.contrib.auth.models import User

from Core.utils.fsm import transition, TransitionMeta
from Procurement.models import BiddingSheet
from Inventory import (
    ENTRYSTATUS_CHOICES,
    ENTRYSTATUS_CHOICES_PUCAHSER,
    ENTRYSTATUS_CHOICES_INSPECTOR,
    ENTRYSTATUS_CHOICES_KEEPER,
    ENTRYSTATUS_CHOICES_END,
    BOUGHTIN_COMPONENT_CHOICES,
    STEEL_TYPES)
from Inventory.models import (
    WeldingMaterialInventoryDetail,
    SteelMaterialInventoryDetail,
    AuxiliaryMaterialInventoryDetail,
    BoughtInComponentInventoryDetail,
    WeldingMaterialEntryDetail,
    SteelMaterialEntryDetail,
    AuxiliaryMaterialEntryDetail,
    BoughtInComponentEntryDetail,
)


class AbstractEntry(models.Model, metaclass=TransitionMeta):
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    # TODO: Auto relate source
    source = models.CharField(verbose_name='货物来源', max_length=20)
    create_dt = models.DateTimeField(verbose_name='入库时间',
                                     auto_now_add=True)
    purchaser = models.ForeignKey(User, verbose_name='采购员',
                                  related_name='%(class)s_purchaser',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检验员',
                                  related_name='%(class)s_inspector',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               related_name='%(class)s_keeper',
                               blank=True, null=True,
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='入库单状态',
                                 choices=ENTRYSTATUS_CHOICES,
                                 default=ENTRYSTATUS_CHOICES_PUCAHSER)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, default='')

    @transition(field='status',
                source=ENTRYSTATUS_CHOICES_PUCAHSER,
                target=ENTRYSTATUS_CHOICES_INSPECTOR, name='采购确认')
    def purchaser_confirm(self, request):
        """
        采购确认
        """
        self.purchaser = request.user

    @transition(field='status',
                source=ENTRYSTATUS_CHOICES_INSPECTOR,
                target=ENTRYSTATUS_CHOICES_KEEPER, name='检查确认')
    def inspector_confirm(self, request):
        """
        检查确认
        """
        self.inspector = request.user

    class Meta:
        abstract = True

    def __str__(self):
        return self.uid

    @staticmethod
    def create_inventory_details(entry_details, InventoryDetailClass,
                                 extra_funcs=None):
        if extra_funcs is None:
            extra_funcs = []
        inventory_details = []
        for entry_detail in entry_details:
            inventory_detail = InventoryDetailClass()
            inventory_detail.weight = entry_detail.weight
            inventory_detail.count = entry_detail.count
            inventory_detail.entry_detail = entry_detail
            for (field_name, extra_func) in extra_funcs:
                field_value = extra_func(entry_detail)
                setattr(inventory_detail, field_name, field_value)
            inventory_details.append(inventory_detail)
        InventoryDetailClass.objects.bulk_create(inventory_details)

    @classmethod
    def create_entry(cls, bidding_sheet, inspections):
        """
        根据表单获取相关上下文, 根据到货检验创建入库单信息
        """
        entry = cls(
            bidding_sheet=bidding_sheet,
            source=bidding_sheet.biddingacceptance.accept_supplier.name)
        entry.save()
        details = []
        for inspection in inspections:
            procurement_material = inspection.material
            detail = cls.entry_detail_cls(
                entry=entry,
                procurement_material=procurement_material,
                weight=procurement_material.weight,
                count=procurement_material.count)
            details.append(detail)
            inspection.entry_confirm()
        cls.entry_detail_cls.objects.bulk_create(details)


class WeldingMaterialEntry(AbstractEntry):
    """
    焊材入库单
    """
    entry_detail_cls = WeldingMaterialEntryDetail

    @transition(field='status',
                source=ENTRYSTATUS_CHOICES_KEEPER,
                target=ENTRYSTATUS_CHOICES_END, name='库管确认')
    def keeper_confirm(self, request):
        """
        库管确认
        """
        self.keeper = request.user
        entry_details = self.details.all()

        def calculate_deadline(entry_detail):
            deadline = entry_detail.production_dt
            deadline = deadline.replace(year=deadline.year+2)
            return deadline

        self.create_inventory_details(
            entry_details, WeldingMaterialInventoryDetail,
            [('deadline', calculate_deadline)])

    class Meta:
        verbose_name = '焊材入库单'
        verbose_name_plural = '焊材入库单'


class SteelMaterialEntry(AbstractEntry):
    """
    钢材入库单
    """
    entry_detail_cls = SteelMaterialEntryDetail
    # TODO: Maybe move this to Detail would be more reasonable
    steel_type = models.IntegerField(verbose_name='材料类型',
                                     choices=STEEL_TYPES)

    @transition(field='status',
                source=ENTRYSTATUS_CHOICES_KEEPER,
                target=ENTRYSTATUS_CHOICES_END, name='库管确认')
    def keeper_confirm(self, request):
        """
        库管确认
        """
        self.keeper = request.user
        entry_details = self.details.all()
        self.create_inventory_details(
            entry_details, SteelMaterialInventoryDetail)

    class Meta:
        verbose_name = '钢材入库单'
        verbose_name_plural = '钢材入库单'


class AuxiliaryMaterialEntry(AbstractEntry):
    """
    辅材入库单
    """
    entry_detail_cls = AuxiliaryMaterialEntryDetail

    @transition(field='status',
                source=ENTRYSTATUS_CHOICES_KEEPER,
                target=ENTRYSTATUS_CHOICES_END, name='库管确认')
    def keeper_confirm(self, request):
        """
        库管确认
        """
        self.keeper = request.user
        entry_details = self.details.all()
        self.create_inventory_details(
            entry_details, AuxiliaryMaterialInventoryDetail)

    class Meta:
        verbose_name = '辅材入库单'
        verbose_name_plural = '辅材入库单'


class BoughtInComponentEntry(AbstractEntry):
    """
    外购件入库单
    """
    entry_detail_cls = BoughtInComponentEntryDetail

    category = models.IntegerField(verbose_name='外购件类型',
                                   choices=BOUGHTIN_COMPONENT_CHOICES)

    @transition(field='status',
                source=ENTRYSTATUS_CHOICES_KEEPER,
                target=ENTRYSTATUS_CHOICES_END, name='库管确认')
    def keeper_confirm(self, request):
        """
        库管确认
        """
        self.keeper = request.user
        entry_details = self.details.all()
        self.create_inventory_details(
            entry_details, BoughtInComponentInventoryDetail)

    class Meta:
        verbose_name = '外购件入库单'
        verbose_name_plural = '外购件入库单'
