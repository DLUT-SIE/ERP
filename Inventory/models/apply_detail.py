from django.db import models

from Procurement.models import ProcurementMaterial


class AbstractApplyDetail(models.Model):
    procurement_material = models.ForeignKey(
        ProcurementMaterial, verbose_name='采购物料',
        blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.procurement_material)


class SteelMaterialApplyDetail(AbstractApplyDetail):
    """
    钢材领用单明细
    """
    apply_card = models.ForeignKey('SteelMaterialApplyCard',
                                   verbose_name='领用单',
                                   related_name='details',
                                   on_delete=models.CASCADE)
    inventory_detail = models.ForeignKey('SteelMaterialInventoryDetail',
                                         verbose_name='库存明细',
                                         blank=True, null=True,
                                         on_delete=models.SET_NULL)
    count = models.IntegerField(verbose_name='申请数量')
    component = models.CharField(verbose_name='零件编号', max_length=100,
                                 blank=True, default='')

    class Meta:
        verbose_name = '钢材领用单明细'
        verbose_name_plural = '钢材领用单明细'


class BoughtInComponentApplyDetail(AbstractApplyDetail):
    """
    外购件领用单明细
    """
    apply_card = models.ForeignKey('BoughtInComponentApplyCard',
                                   verbose_name='领用单',
                                   related_name='details',
                                   on_delete=models.CASCADE)
    inventory_detail = models.ForeignKey('BoughtInComponentInventoryDetail',
                                         verbose_name='库存明细',
                                         blank=True, null=True,
                                         on_delete=models.SET_NULL)
    count = models.IntegerField(verbose_name='数量', default=0)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, default='')

    class Meta:
        verbose_name = '外购件领用单明细'
        verbose_name_plural = '外购件领用单明细'
