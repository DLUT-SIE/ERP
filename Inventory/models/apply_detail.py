from django.db import models

from Core.models import SubWorkOrder
from Procurement.models import ProcurementMaterial


class AbstractApplyDetail(models.Model):
    material = models.ForeignKey(ProcurementMaterial, verbose_name='采购物料',
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class SteelMaterialApplyDetail(AbstractApplyDetail):
    """
    钢材领用单明细
    """
    apply_card = models.ForeignKey('SteelMaterialApplyCard',
                                   verbose_name='领用单',
                                   on_delete=models.CASCADE)
    inventory = models.ForeignKey('SteelMaterialInventoryDetail',
                                  verbose_name='库存明细',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    sub_order = models.ForeignKey(SubWorkOrder, verbose_name='子工作令',
                                  on_delete=models.CASCADE)
    material_mark = models.CharField(verbose_name='钢号', max_length=20)
    material_code = models.CharField(verbose_name='材质编号', max_length=20)
    specification = models.CharField(verbose_name='规格', max_length=50)
    count = models.IntegerField(verbose_name='申请数量')
    component = models.CharField(verbose_name='零件编号', max_length=100,
                                 blank=True, null=True)

    class Meta:
        verbose_name = '钢材领用单明细'
        verbose_name_plural = '钢材领用单明细'

    def __str__(self):
        return '{}({})'.format(self.material_mark, self.specification)


class AuxiliaryMaterialApplyDetail(AbstractApplyDetail):
    """
    辅材领用单明细
    """
    apply_card = models.ForeignKey('AuxiliaryMaterialApplyCard',
                                   verbose_name='领用单',
                                   on_delete=models.CASCADE)
    apply_inventory = models.ForeignKey('AuxiliaryMaterialInventoryDetail',
                                        verbose_name='库存明细',
                                        related_name='apply_inventory',
                                        on_delete=models.CASCADE)
    apply_count = models.IntegerField(verbose_name='申请数量')
    actual_inventory = models.ForeignKey('AuxiliaryMaterialInventoryDetail',
                                         verbose_name='实发材料',
                                         null=True, blank=True,
                                         related_name='actual_inventory',
                                         on_delete=models.SET_NULL)
    actual_count = models.IntegerField(verbose_name='实发数量',
                                       null=True, blank=True)

    class Meta:
        verbose_name = '辅材领用单明细'
        verbose_name_plural = '辅材领用单明细'


class BoughtInComponentApplyDetail(AbstractApplyDetail):
    """
    外购件领用单明细
    """
    apply_card = models.ForeignKey('BoughtInComponentApplyCard',
                                   verbose_name='领用单',
                                   on_delete=models.CASCADE)
    inventory = models.ForeignKey('BoughtInComponentInventoryDetail',
                                  verbose_name='库存明细',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    count = models.IntegerField(verbose_name='数量', default=0)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, null=True)

    class Meta:
        verbose_name = '外购件领用单明细'
        verbose_name_plural = '外购件领用单明细'

    def __str__(self):
        return '{}({})'.format(self.inventory, self.apply_card)
