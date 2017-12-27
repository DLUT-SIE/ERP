from django.db import models
from django.utils import timezone

from Inventory import (INVENTORY_DETAIL_STATUS_CHOICES,
                       INVENTORY_DETAIL_STATUS_NORMAL)


class AbstractInventoryDetail(models.Model):
    # TODO: Review these fields in inventory practice
    weight = models.FloatField(verbose_name='单重')
    count = models.FloatField(verbose_name='数量')
    status = models.IntegerField(verbose_name='状态',
                                 choices=INVENTORY_DETAIL_STATUS_CHOICES,
                                 default=INVENTORY_DETAIL_STATUS_NORMAL)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.entry_detail)


class WeldingInventoryManager(models.Manager):
    def get_queryset(self):
        return super(WeldingInventoryManager, self).get_queryset().filter(
            deadline__gte=timezone.now())


class WeldingMaterialInventoryDetail(AbstractInventoryDetail):
    """
    焊材库存明细
    """
    entry_detail = models.ForeignKey('WeldingMaterialEntryDetail',
                                     verbose_name='焊材入库明细',
                                     on_delete=models.CASCADE)
    deadline = models.DateTimeField(verbose_name='有效期')
    objects = WeldingInventoryManager()

    class Meta:
        verbose_name = '焊材库存明细'
        verbose_name_plural = '焊材库存明细'


class SteelMaterialInventoryDetail(AbstractInventoryDetail):
    """
    钢材库存明细
    """
    entry_detail = models.ForeignKey('SteelMaterialEntryDetail',
                                     verbose_name='钢材入库明细',
                                     on_delete=models.CASCADE)
    length = models.FloatField(verbose_name='长度', default=-1)
    refund_times = models.IntegerField(verbose_name='退库次数', default=0)
    warehouse = models.ForeignKey('Warehouse', verbose_name='库房',
                                  blank=True, null=True,
                                  on_delete=models.PROTECT)

    class Meta:
        verbose_name = '钢材库存明细'
        verbose_name_plural = '钢材库存明细'


class AuxiliaryMaterialInventoryDetail(AbstractInventoryDetail):
    """
    辅材库存明细
    """
    entry_detail = models.ForeignKey('AuxiliaryMaterialEntryDetail',
                                     verbose_name='辅材入库明细',
                                     on_delete=models.CASCADE)

    class Meta:
        verbose_name = '辅材库存明细'
        verbose_name_plural = '辅材库存明细'


class BoughtInComponentInventoryDetail(AbstractInventoryDetail):
    """
    外购件库存明细
    """
    entry_detail = models.OneToOneField('BoughtInComponentEntryDetail',
                                        verbose_name='外购件入库明细',
                                        on_delete=models.CASCADE)

    class Meta:
        verbose_name = '外购件库存明细'
        verbose_name_plural = '外购件库存明细'
