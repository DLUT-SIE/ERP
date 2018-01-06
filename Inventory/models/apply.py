from django.db import models
from django.contrib.auth.models import User

from Core.models import SubWorkOrder
from Core.utils.fsm import transition, TransitionMeta
from Process.models import ProcessMaterial
from Inventory import (
    APPLYCARD_STATUS_CHOICES, APPLYCARD_STATUS_APPLICANT,
    APPLYCARD_STATUS_AUDITOR, APPLYCARD_STATUS_INSPECTOR,
    APPLYCARD_STATUS_KEEPER, APPLYCARD_STATUS_END)
from Inventory.models import (
    SteelMaterialApplyDetail,
    BoughtInComponentApplyDetail,
)


class AbstractApplyCard(models.Model, metaclass=TransitionMeta):
    # TODO: Auto-generated?
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    sub_order = models.ForeignKey(SubWorkOrder, verbose_name='子工作令',
                                  on_delete=models.CASCADE)
    # TODO: ForeignKey?
    department = models.CharField(verbose_name='领用单位', max_length=20,
                                  null=True, default='')
    create_dt = models.DateTimeField(verbose_name='填写时间',
                                     auto_now_add=True)
    applicant = models.ForeignKey(User, verbose_name='领用人',
                                  blank=True, null=True,
                                  related_name='%(class)s_applicant',
                                  on_delete=models.SET_NULL)
    auditor = models.ForeignKey(User, verbose_name='审核人',
                                blank=True, null=True,
                                related_name='%(class)s_auditor',
                                on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检查员',
                                  blank=True, null=True,
                                  related_name='%(class)s_inspector',
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               blank=True, null=True,
                               related_name='%(class)s_keeper',
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='状态',
                                 choices=APPLYCARD_STATUS_CHOICES,
                                 default=APPLYCARD_STATUS_APPLICANT)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, default='')

    class Meta:
        abstract = True

    def __str__(self):
        return self.uid

    @classmethod
    def gen_uid_index(cls):
        """
        返回下一个自增主键
        """
        last = cls.objects.last()
        return 1 if not last else last.id + 1

    @transition(field='status',
                source=APPLYCARD_STATUS_APPLICANT,
                target=APPLYCARD_STATUS_AUDITOR,
                name='领用确认')
    def applicant_confirm(self, request):
        """
        领用确认
        """
        self.applicant = request.user

    @transition(field='status',
                source=APPLYCARD_STATUS_AUDITOR,
                target=APPLYCARD_STATUS_INSPECTOR,
                name='审核确认')
    def auditor_confirm(self, request):
        """
        审核确认
        """
        self.auditor = request.user

    @transition(field='status',
                source=APPLYCARD_STATUS_INSPECTOR,
                target=APPLYCARD_STATUS_KEEPER,
                name='检查确认')
    def inspector_confirm(self, request):
        """
        检查确认
        """
        self.inspector = request.user


class WeldingMaterialApplyCard(AbstractApplyCard):
    """
    焊材领用单
    """
    apply_detail_cls = None
    process_material = models.ForeignKey(
        ProcessMaterial, verbose_name='工艺物料', on_delete=models.CASCADE)
    inventory = models.ForeignKey('WeldingMaterialInventoryDetail',
                                  verbose_name='库存明细',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    # TODO: valid check before applicant_confirm
    apply_weight = models.FloatField(verbose_name='领用重量',
                                     blank=True, null=True)
    apply_count = models.FloatField(verbose_name='领用数量',
                                    blank=True, null=True)
    actual_weight = models.FloatField(verbose_name='实发重量',
                                      blank=True, null=True)
    actual_count = models.FloatField(verbose_name='实发数量',
                                     blank=True, null=True)

    class Meta:
        verbose_name = '焊材领用单'
        verbose_name_plural = '焊材领用单'

    @classmethod
    def create_apply_cards(cls, sub_order, process_materials):
        apply_cards = []
        for process_material in process_materials:
            # TODO: uid?
            apply_card = cls(
                uid='WA-{}'.format(cls.gen_uid_index()),
                sub_order=sub_order,
                process_material=process_material)
            apply_cards.append(apply_card)
        cls.objects.bulk_create(apply_cards)

    def valid_applicant_confirm(self, request):
        """
        领用确认条件: 完成重量和数量的设置
        """
        return not (self.apply_weight is None or self.apply_count is None)

    def valid_keeper_confirm(self, request):
        """
        库管确认条件: 库管已完成相关分配, 且符合条件
        """
        if (self.actual_weight is None or self.actual_count is None
                or self.inventory is None):
            return False
        # TODO: 重量与数量跟库存的比较合法性, 重量是否为常量?
        if self.inventory.count < self.actual_count:
            return False
        return True

    @transition(field='status',
                source=APPLYCARD_STATUS_KEEPER,
                target=APPLYCARD_STATUS_END,
                name='库管确认')
    def keeper_confirm(self, request):
        """
        库管确认
        """
        self.keeper = request.user
        # TODO: 是否只需要减去数量(重量为常数的前提下)
        self.inventory.count -= self.actual_count
        self.inventory.save()


class SteelMaterialApplyCard(AbstractApplyCard):
    """
    钢材领用单
    """
    apply_detail_cls = SteelMaterialApplyDetail

    class Meta:
        verbose_name = '钢材领用单'
        verbose_name_plural = '钢材领用单'

    @classmethod
    def create_apply_cards(cls, sub_order, process_materials):
        apply_card = cls.objects.create(
            uid='SA-{}'.format(cls.gen_uid_index()),
            sub_order=sub_order)
        details = []
        for process_material in process_materials:
            detail = cls.apply_detail_cls(
                process_material=process_material,
                apply_card=apply_card)
            details.append(detail)
        cls.apply_detail_cls.objects.bulk_create(details)

    def valid_applicant_confirm(self, request):
        return not any(detail.count is None for detail in self.details.all())

    def valid_keeper_confirm(self, request):
        details = self.details.all().select_related('inventory_detail')
        for detail in details:
            if not detail.inventory_detail:
                return False
            if detail.inventory_detail.count < detail.count:
                return False
        return True

    @transition(field='status',
                source=APPLYCARD_STATUS_KEEPER,
                target=APPLYCARD_STATUS_END,
                name='库管确认')
    def keeper_confirm(self, request):
        """
        库管确认
        """
        self.keeper = request.user
        details = self.details.all().select_related('inventory_detail')
        for detail in details:
            detail.inventory_detail.count -= detail.count
            detail.inventory_detail.save()


class AuxiliaryMaterialApplyCard(AbstractApplyCard):
    """
    辅材领用单
    """
    apply_inventory = models.ForeignKey('AuxiliaryMaterialInventoryDetail',
                                        verbose_name='库存明细',
                                        related_name='apply_inventory',
                                        blank=True, null=True,
                                        on_delete=models.CASCADE)
    apply_count = models.IntegerField(verbose_name='申请数量',
                                      blank=True, null=True)
    actual_inventory = models.ForeignKey('AuxiliaryMaterialInventoryDetail',
                                         verbose_name='实发材料',
                                         null=True, blank=True,
                                         related_name='actual_inventory',
                                         on_delete=models.SET_NULL)
    actual_count = models.IntegerField(verbose_name='实发数量',
                                       null=True, blank=True)

    class Meta:
        verbose_name = '辅材领用单'
        verbose_name_plural = '辅材领用单'

    @classmethod
    def create_apply_cards(cls, sub_order, process_materials):
        apply_cards = []
        for process_material in process_materials:
            # TODO: uid?
            apply_card = cls(
                uid='AA-{}'.format(cls.gen_uid_index()),
                sub_order=sub_order)
            apply_cards.append(apply_card)
        cls.objects.bulk_create(apply_cards)

    def valid_applicant_confirm(self, request):
        return not (self.apply_inventory is None or self.apply_count is None)

    def valid_keeper_confirm(self, request):
        if self.actual_inventory is None or self.actual_count is None:
            return False
        if self.actual_inventory.count < self.actual_count:
            return False
        return True

    @transition(field='status',
                source=APPLYCARD_STATUS_KEEPER,
                target=APPLYCARD_STATUS_END,
                name='库管确认')
    def keeper_confirm(self, request):
        """
        库管确认
        """
        self.keeper = request.user
        self.actual_inventory.count -= self.actual_count
        self.actual_inventory.save()


class BoughtInComponentApplyCard(AbstractApplyCard):
    """
    外购件领用单
    """
    apply_detail_cls = BoughtInComponentApplyDetail

    revised_number = models.CharField(verbose_name='修订号', max_length=50,
                                      blank=True, default='')
    # TODO: Review these fields
    sample_report = models.CharField(verbose_name='样表', max_length=50,
                                     blank=True, default='')

    class Meta:
        verbose_name = '外购件领用单'
        verbose_name_plural = '外购件领用单'

    @classmethod
    def create_apply_cards(cls, sub_order, process_materials):
        apply_card = cls.objects.create(
            uid='BA-{}'.format(cls.gen_uid_index()),
            sub_order=sub_order)
        details = []
        for process_material in process_materials:
            detail = cls.apply_detail_cls(
                process_material=process_material,
                apply_card=apply_card)
            details.append(detail)
        cls.apply_detail_cls.objects.bulk_create(details)

    def valid_applicant_confirm(self, request):
        return not any(detail.count is None for detail in self.details.all())

    def valid_keeper_confirm(self, request):
        details = self.details.all().select_related('inventory_detail')
        for detail in details:
            if not detail.inventory_detail:
                return False
            if detail.inventory_detail.count < detail.count:
                return False
        return True

    @transition(field='status',
                source=APPLYCARD_STATUS_KEEPER,
                target=APPLYCARD_STATUS_END,
                name='库管确认')
    def keeper_confirm(self, request):
        """
        库管确认
        """
        self.keeper = request.user
        details = self.details.all().select_related('inventory_detail')
        for detail in details:
            detail.inventory_detail.count -= detail.count
            detail.inventory_detail.save()
