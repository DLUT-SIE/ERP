from django.db import models
from django.utils import timezone

from Inventory import (INVENTORY_DETAIL_STATUS_CHOICES,
                       INVENTORY_DETAIL_STATUS_EXHAUST,
                       INVENTORY_DETAIL_STATUS_NORMAL,
                       BOUGHTIN_COMPONENT_CHOICES,
                       BOUGHTIN_COMPONENT_COOPERATION)


class AbstractInventoryDetail(models.Model):
    status = models.IntegerField(verbose_name='状态',
                                 choices=INVENTORY_DETAIL_STATUS_CHOICES,
                                 default=INVENTORY_DETAIL_STATUS_NORMAL)
    # TODO: Review these fields in inventory practice
    weight = models.FloatField(verbose_name='单重', blank=True, null=True)
    count = models.FloatField(verbose_name='数量', blank=True, null=True)
    unit = models.CharField(verbose_name='单位', max_length=20,
                            blank=True, default='')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Update status after refunding
        if (self.count > 0 and
                self.status == INVENTORY_DETAIL_STATUS_EXHAUST):
            self.status = INVENTORY_DETAIL_STATUS_NORMAL
        # Update status after applying
        elif (self.count == 0 and
                self.status == INVENTORY_DETAIL_STATUS_NORMAL):
            self.status = INVENTORY_DETAIL_STATUS_EXHAUST
        super(AbstractInventoryDetail, self).save(*args, **kwargs)

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
    deadline = models.DateField(verbose_name='有效期')
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
    # TODO: blank=False null=False?
    length = models.FloatField(verbose_name='长度')
    refund_times = models.IntegerField(verbose_name='退库次数', default=0)
    warehouse = models.ForeignKey('Warehouse', verbose_name='库房位置',
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
    entry_item = models.OneToOneField('BoughtInComponentEntryDetail',
                                      verbose_name='外购件入库明细',
                                      on_delete=models.CASCADE)
    category = models.IntegerField(verbose_name='外购件类型',
                                   choices=BOUGHTIN_COMPONENT_CHOICES,
                                   default=BOUGHTIN_COMPONENT_COOPERATION)

    class Meta:
        verbose_name = '外购件库存明细'
        verbose_name_plural = '外购件库存明细'
