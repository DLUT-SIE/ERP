from django.db import models
from django.contrib.auth.models import User

from Process import QUOTA_LIST_CATEGORY_CHOICES
from Process.models import Material, ProcessLibrary, ProcessMaterial


class QuotaList(models.Model):
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

    class Meta:
        verbose_name = '定额明细表'
        verbose_name_plural = '定额明细表'

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
    process_material = models.OneToOneField(ProcessMaterial,
                                            verbose_name='工艺物料',
                                            related_name='%(class)s',
                                            on_delete=models.CASCADE)
    quota_coef = models.FloatField(verbose_name='定额系数')
    quota = models.FloatField(verbose_name='定额')
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
    material = models.ForeignKey(Material, verbose_name='材质',
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
