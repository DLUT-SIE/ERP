from django.db import models
from django.contrib.auth.models import User

from Inventory import REFUNDSTATUS_CHOICES, REFUNDSTATUS_REFUNDER


class AbstractRefundCard(models.Model):
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    created = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
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


class SteelMaterialRefundCard(AbstractRefundCard):
    """
    钢材退库单
    """
    # TODO: OneToOne?
    apply_card = models.ForeignKey('SteelMaterialApplyCard',
                                   verbose_name='领用单',
                                   blank=True, null=True,
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = '钢材退库单'
        verbose_name_plural = '钢材退库单'


class WeldingMaterialRefundCard(AbstractRefundCard):
    """
    焊材退库单
    """
    # TODO: ForeignKey?
    apply_card = models.OneToOneField('WeldingMaterialApplyCard',
                                      verbose_name='领用单',
                                      on_delete=models.CASCADE)
    weight = models.FloatField(verbose_name='退库量（重量）')
    count = models.FloatField(verbose_name='退库量（数量）',
                              null=True, blank=True)

    class Meta:
        verbose_name = '焊材退库单'
        verbose_name_plural = '焊材退库单'

    def __str__(self):
        return str(self.apply_card)


class BoughtInComponentRefundCard(AbstractRefundCard):
    """
    外购件退库单
    """
    apply_card = models.ForeignKey('BoughtInComponentApplyCard',
                                   verbose_name='领用单',
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = '外购件退库单'
        verbose_name_plural = '外购件退库单'
