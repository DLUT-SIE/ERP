from django.db import models

from Procurement.models import ProcurementMaterial


class AbstractEntryDetail(models.Model):
    material = models.ForeignKey(ProcurementMaterial, verbose_name='采购物料',
                                 blank=True, null=True,
                                 on_delete=models.CASCADE)
    weight = models.FloatField(verbose_name='单重')
    count = models.FloatField(verbose_name='数量')
    unit = models.CharField(verbose_name='单位', max_length=20,
                            blank=True, default='')
    factory = models.CharField(verbose_name='厂家', max_length=100,
                               blank=True, default='')
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, default='')

    class Meta:
        abstract = True

    def __str__(self):
        return '{}-{}'.format(self.entry, self.material)


class WeldingMaterialEntryDetail(AbstractEntryDetail):
    """
    焊材入库单明细
    """
    entry = models.ForeignKey('WeldingMaterialEntry', verbose_name='入库单',
                              on_delete=models.CASCADE)
    production_date = models.DateField(verbose_name='出厂日期',
                                       blank=True, null=True)

    class Meta:
        verbose_name = '焊材入库单明细'
        verbose_name_plural = '焊材入库单明细'

    def __str__(self):
        return '{}-{}'.format(self.entry, self.material)


class SteelMaterialEntryDetail(AbstractEntryDetail):
    """
    钢材入库单明细
    """
    entry = models.ForeignKey('SteelMaterialEntry', verbose_name='入库单',
                              on_delete=models.CASCADE)
    length = models.FloatField(verbose_name='长度')

    class Meta:
        verbose_name = '钢材入库单明细'
        verbose_name_plural = '钢材入库单明细'


class AuxiliaryMaterialEntryDetail(AbstractEntryDetail):
    """
    辅材入库单明细
    """
    entry = models.ForeignKey('AuxiliaryMaterialEntry', verbose_name='入库单',
                              on_delete=models.CASCADE)

    class Meta:
        verbose_name = '辅材入库单明细'
        verbose_name_plural = '辅材入库单明细'


class BoughtInComponentEntryDetail(AbstractEntryDetail):
    """
    外购件入库单明细
    """
    entry = models.ForeignKey('BoughtInComponentEntry', verbose_name='入库单',
                              on_delete=models.CASCADE)

    class Meta:
        verbose_name = '外购件入库单明细'
        verbose_name_plural = '外购件入库单明细'
