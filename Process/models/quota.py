from django.db import models
from django.contrib.auth.models import User

from Process import (
    QUOTA_LIST_CATEGORY_CHOICES, QUOTASTATUS_CHOICES, QUOTASTATUS_INIT,
    QUOTASTATUS_WRITTEN, QUOTASTATUS_RIVIEWED, QUOTA_LIST_CATEGORY_AUXILIARY,
    QUOTA_LIST_CATEGORY_PRINCIPAL, QUOTA_LIST_CATEGORY_COOPERANT,
    QUOTA_LIST_CATEGORY_FIRSTFEEDING, QUOTA_LIST_CATEGORY_OUTPURCHASED,
    QUOTA_LIST_CATEGORY_WELDQUOTAPAGE)
from Process.models import (
    Material, ProcessLibrary, ProcessMaterial, TotalWeldingMaterial)
from Core.utils.fsm import transition, TransitionMeta
from Procurement.models import ProcurementMaterial


class QuotaList(models.Model, metaclass=TransitionMeta):
    """
    定额明细表
    """
    lib = models.ForeignKey(ProcessLibrary, verbose_name='工艺库',
                            on_delete=models.CASCADE)
    writer = models.ForeignKey(User, verbose_name='编制人',
                               blank=True, null=True,
                               related_name='quota_list_writer',
                               on_delete=models.SET_NULL)
    # TODO: auto_now_add?
    write_dt = models.DateTimeField(verbose_name='编制日期',
                                    blank=True, null=True)
    reviewer = models.ForeignKey(User, verbose_name='审核人',
                                 blank=True, null=True,
                                 related_name='quota_list_reviewer',
                                 on_delete=models.SET_NULL)
    review_dt = models.DateTimeField(verbose_name='审核日期', blank=True,
                                     null=True)
    category = models.IntegerField(verbose_name='明细表类别',
                                   choices=QUOTA_LIST_CATEGORY_CHOICES)
    status = models.IntegerField(verbose_name='定额明细表编制状态',
                                 choices=QUOTASTATUS_CHOICES,
                                 default=QUOTASTATUS_INIT)

    class Meta:
        verbose_name = '定额明细表'
        verbose_name_plural = '定额明细表'

    @transition(field='status',
                source=QUOTASTATUS_INIT,
                target=QUOTASTATUS_WRITTEN,
                name='编制确认')
    def quota_write(self, request):
        self.writer = request.user

    def createProcurementMaterial(self):
        work_order = self.lib.work_order
        inventory_type = self.category
        quotaclass = None
        abstract_item = False
        procurement_material_list = []
        if inventory_type == QUOTA_LIST_CATEGORY_AUXILIARY:
            quotaclass = AuxiliaryQuotaItem
        elif inventory_type == QUOTA_LIST_CATEGORY_PRINCIPAL:
            quotaclass = PrincipalQuotaItem
        elif inventory_type == QUOTA_LIST_CATEGORY_WELDQUOTAPAGE:
            quotaclass = WeldingQuotaItem
        else:
            abstract_item = True
            if inventory_type == QUOTA_LIST_CATEGORY_COOPERANT:
                quotaclass = CooperantItem
            elif inventory_type == QUOTA_LIST_CATEGORY_FIRSTFEEDING:
                quotaclass = FirstFeedingItem
            elif inventory_type == QUOTA_LIST_CATEGORY_OUTPURCHASED:
                quotaclass = BoughtInItem
        if abstract_item:
            for sub_order in work_order.subworkorder_set.all():
                for item in quotaclass.objects.filter(
                        quota_list=self):
                    procurement_material = ProcurementMaterial()
                    procurement_material.process_material = \
                        item.process_material
                    procurement_material.sub_order = sub_order
                    procurement_material.inventory_type = self.category
                    procurement_material.material_number = \
                        item.process_material.material.uid
                    procurement_material.category = \
                        item.process_material.material.category
                    procurement_material.count = item.process_material.count
                    procurement_material.weight = item.process_material.weight
                    procurement_material_list.append(procurement_material)
        else:
            for sub_order in work_order.subworkorder_set.all():
                for item in quotaclass.objects.filter(
                        quota_list=self):
                    procurement_material = ProcurementMaterial()
                    procurement_material.sub_order = sub_order
                    procurement_material.inventory_type = self.category
                    procurement_material.material_number = item.material.uid
                    procurement_material.category = item.material.category
                    procurement_material.count = item.count
                    procurement_material.weight = item.weight
                    procurement_material_list.append(procurement_material)
        ProcurementMaterial.objects.bulk_create(procurement_material_list)

    @transition(field='status',
                source=QUOTASTATUS_WRITTEN,
                target=QUOTASTATUS_RIVIEWED,
                name='审核确认')
    def quota_review(self, request):
        self.reviewer = request.user
        self.createProcurementMaterial()

    def __str__(self):
        return str(self.lib)


class AbstractQuotaItem(models.Model):
    """
    定额基类
    """
    quota_list = models.ForeignKey(QuotaList, verbose_name='定额明细表',
                                   on_delete=models.CASCADE)
    process_material = models.OneToOneField(ProcessMaterial,
                                            verbose_name='工艺物料',
                                            related_name='%(class)s',
                                            on_delete=models.CASCADE)
    remark = models.CharField(verbose_name='备注', max_length=50,
                              blank=True, default='')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.process_material)


class AuxiliaryQuotaItem(AbstractQuotaItem):
    """
    辅材定额
    """

    quota_coef = models.FloatField(verbose_name='定额系数', blank=True,
                                   null=True)
    quota = models.FloatField(verbose_name='定额', blank=True, null=True)
    stardard_code = models.CharField(verbose_name='标准代码', max_length=50,
                                     blank=True, default='')
    # TODO: choices?
    category = models.CharField(verbose_name='类别', max_length=50,
                                blank=True, default='')

    class Meta:
        verbose_name = '辅材定额'
        verbose_name_plural = '辅材定额'


class CooperantItem(AbstractQuotaItem):
    """
    外协件
    """
    class Meta:
        verbose_name = '外协件'
        verbose_name_plural = '外协件'


class FirstFeedingItem(AbstractQuotaItem):
    """
    先投件
    """
    class Meta:
        verbose_name = '先投件'
        verbose_name_plural = '先投件'


class BoughtInItem(AbstractQuotaItem):
    """
    外购件
    """
    class Meta:
        verbose_name = '外购件'
        verbose_name_plural = '外购件'


class PrincipalQuotaItem(models.Model):
    """
    主材定额
    """
    quota_list = models.ForeignKey(QuotaList, verbose_name='定额明细表',
                                   on_delete=models.CASCADE)
    size = models.CharField(verbose_name='规格', max_length=50,
                            blank=True, default='')
    count = models.IntegerField(verbose_name='数量')
    weight = models.FloatField(verbose_name='单重')
    material = models.ForeignKey(Material, verbose_name='材质',
                                 null=True, blank=True,
                                 on_delete=models.PROTECT)
    operative_norm = models.CharField(verbose_name='执行标准', max_length=50,
                                      blank=True, default='')
    # TODO: Better name? And necessary?
    status = models.CharField(verbose_name='供货状态', max_length=50,
                              blank=True, default='')
    remark = models.CharField(verbose_name='备注', max_length=50,
                              blank=True, default='')

    class Meta:
        verbose_name = '主材定额'
        verbose_name_plural = '主材定额'


class WeldingQuotaItem(models.Model):
    """
    焊材定额
    """

    quota_list = models.ForeignKey(QuotaList, verbose_name='定额明细表',
                                   on_delete=models.CASCADE)
    material = models.ForeignKey(TotalWeldingMaterial,
                                 verbose_name='材质',
                                 on_delete=models.PROTECT)
    size = models.CharField(verbose_name='规格', max_length=50,
                            blank=True, default='')
    quota = models.FloatField(verbose_name='定额')
    remark = models.CharField(verbose_name='备注', blank=True, default='',
                              max_length=50)
    operative_norm = models.CharField(verbose_name='执行标准', max_length=50,
                                      blank=True, default='')

    class Meta:
        verbose_name = '焊材定额'
        verbose_name_plural = '焊材定额'

    def __str__(self):
        return '{}({})'.format(self.material, self.size)
