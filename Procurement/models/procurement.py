from django.db import models
from django.contrib.auth.models import User

from Core.models import WorkOrder, SubWorkOrder
from Process.models import ProcessMaterial
from Procurement import (INVENTORY_TYPE, INVENTORY_TYPE_NOTSET,
                         PURCHASE_ORDER_STATUS_CHOICES)


class PurchaseOrder(models.Model):
    """
    订购单
    """
    uid = models.CharField(verbose_name='编号', max_length=20, unique=True)
    work_order = models.ForeignKey(WorkOrder, verbose_name='工作令')
    create_date = models.DateTimeField(verbose_name='创建日期',
                                       auto_now_add=True)
    status = models.IntegerField(verbose_name='订购单状态',
                                 choices=PURCHASE_ORDER_STATUS_CHOICES)
    lister = models.ForeignKey(User, verbose_name='编制人',
                               related_name='purchase_order_lister',
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    list_date = models.DateTimeField(verbose_name='编制日期',
                                     blank=True, null=True)
    chief = models.ForeignKey(User, verbose_name='外采科长',
                              related_name='purchase_order_chief',
                              null=True, blank=True,
                              on_delete=models.SET_NULL)
    audit_date = models.DateTimeField(verbose_name='审核日期',
                                      blank=True, null=True)
    approver = models.ForeignKey(User, verbose_name='批准人',
                                 related_name='purchase_order_approver',
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL)
    approve_time = models.DateTimeField(verbose_name='批准日期',
                                        blank=True, null=True)
    tech_requirement = models.TextField(verbose_name='工艺需求',
                                        max_length=1000,
                                        blank=True, default='')
    # TODO: choices?
    category = models.IntegerField(verbose_name='标单类型')
    revised_number = models.CharField(verbose_name='修订号', max_length=50,
                                      blank=True, default='')

    class Meta:
        verbose_name = '订购单'
        verbose_name_plural = '订购单'

    def __str__(self):
        return self.uid


class ProcurementMaterial(models.Model):
    """
    采购物料

    process_material为空代表为合并的物料
    """
    process_material = models.ForeignKey(ProcessMaterial,
                                         verbose_name='工艺物料',
                                         null=True, blank=True,
                                         on_delete=models.CASCADE)
    merged_material = models.ForeignKey('self', verbose_name='合并后物料',
                                        null=True, blank=True,
                                        on_delete=models.SET_NULL)
    purchase_order = models.ForeignKey(PurchaseOrder,
                                       verbose_name='订购单',
                                       null=True, blank=True,
                                       on_delete=models.SET_NULL)
    sub_order = models.ForeignKey(SubWorkOrder, verbose_name='子工作令',
                                  on_delete=models.CASCADE)
    inventory_type = models.IntegerField(verbose_name='明细类型',
                                         choices=INVENTORY_TYPE,
                                         default=INVENTORY_TYPE_NOTSET)
    batch_number = models.CharField(verbose_name='炉批号', max_length=50,
                                    blank=True, default='')
    material_number = models.CharField(verbose_name='材质编号', max_length=50,
                                       blank=True, default='')
    delivery_dt = models.DateTimeField(verbose_name='交货期',
                                       blank=True, null=True)
    category = models.CharField(verbose_name='材料分类', max_length=50,
                                blank=True, default='')
    finished = models.BooleanField(verbose_name='是否结束', default=False)
    add_to_detail = models.BooleanField(verbose_name='已加入物料汇总',
                                        default=False)

    class Meta:
        verbose_name = '采购物料'
        verbose_name_plural = '采购物料'

    def __str__(self):
        return '{} {}'.format(self.sub_order, self.process_material)