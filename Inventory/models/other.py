from django.db import models
from django.contrib.auth.models import User

from Inventory import (WAREHOUSE_TYPE_CHOICES, MATERIAL_CATEGORY_CHOICES,
                       INVENTORY_CARD_TYPE_CHOICES)


class Warehouse(models.Model):
    """
    库房
    """
    name = models.CharField(verbose_name='名称', max_length=20)
    location = models.CharField(verbose_name='位置', max_length=50,
                                blank=True, default='')
    category = models.IntegerField(verbose_name='库存类型',
                                   choices=WAREHOUSE_TYPE_CHOICES)

    class Meta:
        verbose_name = '库房'
        verbose_name_plural = '库房'

    def __str__(self):
        return self.name


class WeldingMaterialHumitureRecord(models.Model):
    """
    焊材库温湿度记录卡
    """
    keeper = models.ForeignKey(User, verbose_name='记录人',
                               on_delete=models.CASCADE)
    create_dt = models.DateTimeField(verbose_name='记录时间',
                                     auto_now_add=True)
    actual_temp_1 = models.FloatField(verbose_name='实际温度(10:00)')
    actual_humid_1 = models.FloatField(verbose_name='实际湿度(10:00)')
    actual_temp_2 = models.FloatField(verbose_name='实际温度(16:00)')
    actual_humid_2 = models.FloatField(verbose_name='实际湿度(16:00)')
    remark = models.CharField(verbose_name='备注', max_length=1000,
                              blank=True, default='')

    def __str__(self):
        return '{}({})'.format(self.create_dt, self.keeper)

    class Meta:
        verbose_name = '焊材库温湿度记录卡'
        verbose_name_plural = '焊材库温湿度记录卡'


class WeldingMaterialBakeRecord(models.Model):
    """
    焊材烘焙记录卡
    """
    create_dt = models.DateTimeField(verbose_name='记录时间',
                                     auto_now_add=True)
    standard_num = models.CharField(verbose_name='标准号', max_length=50,
                                    blank=True, default='')
    size = models.CharField(verbose_name='规格', max_length=50,
                            blank=True, default='')
    class_num = models.CharField(verbose_name='牌号', max_length=50)
    heat_num = models.CharField(verbose_name='炉批号', max_length=50)
    codedmark = models.CharField(verbose_name='编码标记', max_length=50,
                                 blank=True, default='')
    quantity = models.FloatField(verbose_name='数量', default=0)
    furnace_time = models.DateTimeField(verbose_name='进炉时间',
                                        blank=True, null=True)
    baking_temp = models.FloatField(verbose_name='烘焙温度', default=0)
    heating_time = models.DateTimeField(verbose_name='到达温度时间',
                                        blank=True, null=True)
    cooling_time = models.DateTimeField(verbose_name='降温时间',
                                        blank=True, null=True)
    # TODO: verbose_name?
    holding_time = models.DateTimeField(verbose_name='进保温炉时间',
                                        blank=True, null=True)
    holding_temp = models.FloatField(verbose_name='保温温度', default=0)
    apply_time = models.DateTimeField(verbose_name='领用时间',
                                      blank=True, null=True)
    keeper = models.ForeignKey(User, verbose_name='库管员',
                               related_name='welding_bake_keeper',
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    welding_engineer = models.ForeignKey(User, verbose_name='焊接工程师',
                                         related_name='welding_bake_engineer',
                                         blank=True, null=True,
                                         on_delete=models.SET_NULL)
    remark = models.CharField(verbose_name='备注', max_length=200,
                              blank=True, default='')

    def __str__(self):
        return str(self.create_dt)

    class Meta:
        verbose_name = '焊材烘焙记录卡'
        verbose_name_plural = '焊材烘焙记录卡'


class WeldingWarehouseThreshold(models.Model):
    """
    焊材库存安全量
    """
    specification = models.CharField(verbose_name='规格', max_length=50)
    count = models.FloatField(verbose_name='数量')
    category = models.IntegerField(verbose_name='材料种类',
                                   choices=MATERIAL_CATEGORY_CHOICES)

    class Meta:
        verbose_name = '焊材库存安全量'
        verbose_name_plural = '焊材库存安全量'

    def __str__(self):
        return self.specification


class InventoryTerminationRecord(models.Model):
    """
    库存单据终止记录
    """
    user = models.ForeignKey(User, verbose_name='操作者',
                             on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='日期', auto_now_add=True)
    category = models.IntegerField(verbose_name='单据类型',
                                   choices=INVENTORY_CARD_TYPE_CHOICES)
    uid = models.CharField(verbose_name='单据ID', max_length=20, unique=True)
    reason = models.CharField(verbose_name='原因', max_length=200)

    class Meta:
        verbose_name = '库存单据终止记录'
        verbose_name_plural = '库存单据终止记录'

    def __str__(self):
        return '{}({})'.format(self.uid, self.category)
