from django.db import models
from django.contrib.auth.models import User

from Procurement.models import BiddingSheet
from Inventory import (ENTRYSTATUS_CHOICES, ENTRYSTATUS_CHOICES_PUCAHSER,
                       BOUGHTIN_COMPONENT_CHOICES, STEEL_TYPES)


class AbstractEntry(models.Model):
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    # TODO: Auto relate source
    source = models.CharField(verbose_name='货物来源', max_length=20)
    create_dt = models.DateTimeField(verbose_name='入库时间',
                                     auto_now_add=True)
    purchaser = models.ForeignKey(User, verbose_name='采购员',
                                  related_name='%(class)s_purchaser',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    inspector = models.ForeignKey(User, verbose_name='检验员',
                                  related_name='%(class)s_inspector',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               related_name='%(class)s_keeper',
                               blank=True, null=True,
                               on_delete=models.SET_NULL)
    status = models.IntegerField(verbose_name='入库单状态',
                                 choices=ENTRYSTATUS_CHOICES,
                                 default=ENTRYSTATUS_CHOICES_PUCAHSER)
    remark = models.CharField(verbose_name='备注', max_length=100,
                              blank=True, default='')

    class Meta:
        abstract = True

    def __str__(self):
        return self.uid


class WeldingMaterialEntry(AbstractEntry):
    """
    焊材入库单
    """
    class Meta:
        verbose_name = '焊材入库单'
        verbose_name_plural = '焊材入库单'


class SteelMaterialEntry(AbstractEntry):
    """
    钢材入库单
    """
    # TODO: Maybe move this to Detail would be more reasonable
    steel_type = models.IntegerField(verbose_name='材料类型',
                                     choices=STEEL_TYPES)

    class Meta:
        verbose_name = '钢材入库单'
        verbose_name_plural = '钢材入库单'


class AuxiliaryMaterialEntry(AbstractEntry):
    """
    辅材入库单
    """
    class Meta:
        verbose_name = '辅材入库单'
        verbose_name_plural = '辅材入库单'


class BoughtInComponentEntry(AbstractEntry):
    """
    外购件入库单
    """
    category = models.IntegerField(verbose_name='外购件类型',
                                   choices=BOUGHTIN_COMPONENT_CHOICES)

    class Meta:
        verbose_name = '外购件入库单'
        verbose_name_plural = '外购件入库单'
