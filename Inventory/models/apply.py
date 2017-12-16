from django.db import models
from django.contrib.auth.models import User

from Core.models import SubWorkOrder
from Procurement.models import ProcurementMaterial
from Inventory import APPLYCARD_STATUS_CHOICES, APPLYCARD_STATUS_APPLICANT


class AbstractApplyCard(models.Model):
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


class WeldingMaterialApplyCard(AbstractApplyCard):
    """
    焊材领用单
    """
    procurement_material = models.ForeignKey(
        ProcurementMaterial, verbose_name='采购物料',
        blank=True, null=True, on_delete=models.SET_NULL)
    inventory = models.ForeignKey('WeldingMaterialInventoryDetail',
                                  verbose_name='库存明细',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    apply_weight = models.FloatField(verbose_name='领用重量')
    apply_count = models.FloatField(verbose_name='领用数量')
    actual_weight = models.FloatField(verbose_name='实发重量',
                                      blank=True, null=True)
    actual_count = models.FloatField(verbose_name='实发数量',
                                     blank=True, null=True)

    class Meta:
        verbose_name = '焊材领用单'
        verbose_name_plural = '焊材领用单'

    def __str__(self):
        return '{}({})'.format(self.material_mark, self.specification)


class SteelMaterialApplyCard(AbstractApplyCard):
    """
    钢材领用单
    """
    class Meta:
        verbose_name = '钢材领用单'
        verbose_name_plural = '钢材领用单'


class AuxiliaryMaterialApplyCard(AbstractApplyCard):
    """
    辅材领用单
    """
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
        verbose_name = '辅材领用单'
        verbose_name_plural = '辅材领用单'


class BoughtInComponentApplyCard(AbstractApplyCard):
    """
    外购件领用单
    """
    revised_number = models.CharField(verbose_name='修订号', max_length=50,
                                      blank=True, default='')
    # TODO: Review these fields
    sample_report = models.CharField(verbose_name='样表', max_length=50,
                                     blank=True, default='')

    class Meta:
        verbose_name = '外购件领用单'
        verbose_name_plural = '外购件领用单'
