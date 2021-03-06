from django.db import models

from Core.utils import DynamicHashPath


class AbstractSteelMaterialRefundDetail(models.Model):
    apply_detail = models.ForeignKey('SteelMaterialApplyDetail',
                                     verbose_name='领用明细',
                                     on_delete=models.CASCADE)
    # TODO: necessary?
    status = models.CharField(verbose_name='状态', max_length=20,
                              blank=True, default='')
    # TODO: Duplicate? Where are these fields?
    specification = models.CharField(verbose_name='规格', max_length=50,
                                     blank=True, default='')
    count = models.IntegerField(verbose_name='数量')
    weight = models.FloatField(verbose_name='重量', blank=True, null=True)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, default='')

    def __str__(self):
        return str(self.apply_detail)


class BoardSteelMaterialRefundDetail(AbstractSteelMaterialRefundDetail):
    """
    板材退库单明细
    """
    refund_card = models.ForeignKey('SteelMaterialRefundCard',
                                    verbose_name='退库单',
                                    related_name='board_details',
                                    on_delete=models.CASCADE)
    graph_path = models.FileField(
        verbose_name='套料图', blank=True, null=True,
        upload_to=DynamicHashPath('BoardSteelMaterialRefundDetail'))

    class Meta:
        verbose_name = '板材退库单明细'
        verbose_name_plural = '板材退库单明细'


class BarSteelMaterialRefundDetail(AbstractSteelMaterialRefundDetail):
    """
    型材退库单明细
    """
    refund_card = models.ForeignKey('SteelMaterialRefundCard',
                                    verbose_name='退库单',
                                    related_name='bar_details',
                                    on_delete=models.CASCADE)
    length = models.FloatField(verbose_name='退库长度', blank=True, null=True)

    class Meta:
        verbose_name = '型材退库单明细'
        verbose_name_plural = '型材退库单明细'


class BoughtInComponentRefundDetail(models.Model):
    """
    外购件退库单明细
    """
    refund_card = models.ForeignKey('BoughtInComponentRefundCard',
                                    verbose_name='退库单',
                                    related_name='details',
                                    on_delete=models.CASCADE)
    apply_detail = models.ForeignKey('BoughtInComponentApplyDetail',
                                     verbose_name='领用明细',
                                     on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='数量')
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, default='')

    class Meta:
        verbose_name = '外购件退库单明细'
        verbose_name_plural = '外购件退库单明细'

    def __str__(self):
        return '{}({})'.format(self.apply_detail, self.refund_card)
