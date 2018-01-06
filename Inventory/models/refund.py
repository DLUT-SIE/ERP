from itertools import chain

from django.db import models
from django.contrib.auth.models import User

from Core.utils.fsm import transition, TransitionMeta
from Inventory import (
    REFUNDSTATUS_CHOICES, REFUNDSTATUS_REFUNDER,
    REFUNDSTATUS_INSPECTOR, REFUNDSTATUS_KEEPER,
    REFUNDSTATUS_END, STEEL_TYPE_BOARD_STEEL,
    STEEL_TYPE_BAR_STEEL,
)
from Inventory.models import (
    SteelMaterialInventoryDetail, BoardSteelMaterialRefundDetail,
    BarSteelMaterialRefundDetail, BoughtInComponentRefundDetail,
    WeldingMaterialApplyCard, SteelMaterialApplyCard,
    BoughtInComponentApplyCard,
)


class AbstractRefundCard(models.Model, metaclass=TransitionMeta):
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    create_dt = models.DateTimeField(verbose_name='创建日期',
                                     auto_now_add=True)
    refunder = models.ForeignKey(User, verbose_name='退料人',
                                 blank=True, null=True,
                                 related_name='%(class)s_refunder',
                                 on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检查员',
                                  blank=True, null=True,
                                  related_name='%(class)s_inspector',
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               blank=True, null=True,
                               related_name='%(class)s_keeper',
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='退库单状态',
                                 choices=REFUNDSTATUS_CHOICES,
                                 default=REFUNDSTATUS_REFUNDER)

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
        if not last:
            return 1
        else:
            return last.id + 1

    @transition(field='status',
                source=REFUNDSTATUS_REFUNDER,
                target=REFUNDSTATUS_INSPECTOR,
                name='退库确认')
    def refunder_confirm(self, request):
        self.refunder = request.user

    @transition(field='status',
                source=REFUNDSTATUS_INSPECTOR,
                target=REFUNDSTATUS_KEEPER,
                name='检查确认')
    def inspector_confirm(self, request):
        self.inspector = request.user


class WeldingMaterialRefundCard(AbstractRefundCard):
    """
    焊材退库单
    """
    apply_cls = WeldingMaterialApplyCard
    apply_card = models.OneToOneField('WeldingMaterialApplyCard',
                                      verbose_name='领用单',
                                      on_delete=models.CASCADE)
    # TODO: 哪个字段是不必要的字段?
    weight = models.FloatField(verbose_name='退库量（重量）',
                               blank=True, null=True)
    count = models.FloatField(verbose_name='退库量（数量）',
                              null=True, blank=True)

    class Meta:
        verbose_name = '焊材退库单'
        verbose_name_plural = '焊材退库单'

    def __str__(self):
        return str(self.apply_card)

    @classmethod
    def create_refund_cards(cls, apply_card, details_dict):
        count = list(details_dict.values())[0]
        cls.objects.create(
            uid='WR-{}'.format(cls.gen_uid_index()),
            apply_card=apply_card,
            count=count)

    def valid_refunder_confirm(self, request):
        """
        退库确认先验条件, 退库数量不能大于领用数量
        """
        if (self.count is None or self.weight is None
                or self.count > self.apply_card.actual_count):
            return False
        return True

    @transition(field='status',
                source=REFUNDSTATUS_KEEPER,
                target=REFUNDSTATUS_END,
                name='库管确认')
    def keeper_confirm(self, request):
        self.keeper = request.user
        inventory_detail = self.apply_card.inventory
        inventory_detail.count += self.count
        inventory_detail.save()


class SteelMaterialRefundCard(AbstractRefundCard):
    """
    钢材退库单
    """
    apply_cls = SteelMaterialApplyCard
    detail_cls = {
        STEEL_TYPE_BAR_STEEL: BarSteelMaterialRefundDetail,
        STEEL_TYPE_BOARD_STEEL: BoardSteelMaterialRefundDetail,
    }

    apply_card = models.ForeignKey('SteelMaterialApplyCard',
                                   verbose_name='领用单',
                                   blank=True, null=True,
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = '钢材退库单'
        verbose_name_plural = '钢材退库单'

    @classmethod
    def create_refund_cards(cls, apply_card, details_dict):
        refund_card = cls.objects.create(
            uid='SR-{}'.format(cls.gen_uid_index()),
            apply_card=apply_card)
        refund_details = {
            STEEL_TYPE_BAR_STEEL: [],
            STEEL_TYPE_BOARD_STEEL: [],
        }
        for apply_detail, count in details_dict.items():
            entry_detail = apply_detail.inventory_detail.entry_detail
            steel_type = entry_detail.entry.steel_type
            refund_detail_cls = cls.detail_cls[steel_type]
            refund_detail = refund_detail_cls(
                refund_card=refund_card,
                apply_detail=apply_detail,
                count=count)
            refund_details[steel_type].append(refund_detail)
        for steel_type, details in refund_details.items():
            cls.detail_cls[steel_type].objects.bulk_create(details)

    def valid_refunder_confirm(self, request):
        for refund_detail in self.board_details.select_related('apply_detail'):
            if refund_detail.count > refund_detail.apply_detail.count:
                return False
        for refund_detail in self.bar_details.select_related(
                'apply_detail', 'apply_detail__inventory_detail'):
            if (refund_detail.count > refund_detail.apply_detail.count or
                    refund_detail.length > refund_detail.apply_detail
                    .inventory_detail.length):
                return False
        return True

    @transition(field='status',
                source=REFUNDSTATUS_KEEPER,
                target=REFUNDSTATUS_END,
                name='库管确认')
    def keeper_confirm(self, request):
        """
        根据退库明细创建新的库存明细
        """
        self.keeper = request.user
        for refund_detail in chain(
                self.board_details.select_related(
                    'apply_detail',
                    'apply_detail__inventory_detail'),
                self.bar_details.select_related(
                    'apply_detail',
                    'apply_detail__inventory_detail')):
            old_inventory_detail = refund_detail.apply_detail.inventory_detail
            SteelMaterialInventoryDetail.objects.create(
                entry_detail=old_inventory_detail.entry_detail,
                weight=refund_detail.weight,
                count=refund_detail.count,
                length=getattr(refund_detail, 'length', -1),
                refund_times=old_inventory_detail.refund_times+1)


class BoughtInComponentRefundCard(AbstractRefundCard):
    """
    外购件退库单
    """
    apply_cls = BoughtInComponentApplyCard
    detail_cls = BoughtInComponentRefundDetail
    apply_card = models.ForeignKey('BoughtInComponentApplyCard',
                                   verbose_name='领用单',
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = '外购件退库单'
        verbose_name_plural = '外购件退库单'

    @classmethod
    def create_refund_cards(cls, apply_card, details_dict):
        refund_card = cls.objects.create(
            uid='BR-{}'.format(cls.gen_uid_index()),
            apply_card=apply_card)
        refund_details = []
        for apply_detail, count in details_dict.items():
            refund_detail = cls.detail_cls(
                refund_card=refund_card,
                apply_detail=apply_detail,
                count=count)
            refund_details.append(refund_detail)
        cls.detail_cls.objects.bulk_create(refund_details)

    def valid_refunder_confirm(self, request):
        for refund_detail in self.details.select_related('apply_detail'):
            if refund_detail.count > refund_detail.apply_detail.count:
                return False
        return True

    @transition(field='status',
                source=REFUNDSTATUS_KEEPER,
                target=REFUNDSTATUS_END,
                name='库管确认')
    def keeper_confirm(self, request):
        self.keeper = request.user
        for refund_detail in self.details.select_related('apply_detail'):
            inventory_detail = refund_detail.apply_detail.inventory_detail
            inventory_detail.count += refund_detail.count
            inventory_detail.save()
