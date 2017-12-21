from django.db import models
from django.contrib.auth.models import User

from Core.models import WorkOrder
from Process import MATERIAL_CATEGORY_CHOICES


class Material(models.Model):
    """
    材质
    """
    name = models.CharField(verbose_name='材质名称', max_length=50)
    uid = models.CharField(verbose_name='材质编号', unique=True, max_length=20)
    category = models.IntegerField(verbose_name='材质类别',
                                   blank=True, null=True,
                                   choices=MATERIAL_CATEGORY_CHOICES)

    class Meta:
        verbose_name = '材质'
        verbose_name_plural = '材质'

    def __str__(self):
        return self.name


class ProcessLibrary(models.Model):
    """
    工艺库

    保存工作令相关工艺公共信息
    """
    work_order = models.OneToOneField(WorkOrder, verbose_name='工作令',
                                      on_delete=models.CASCADE,
                                      related_name='process_library')

    writer = models.ForeignKey(User, verbose_name='工艺员',
                               blank=True, null=True,
                               related_name='process_lib_writer',
                               on_delete=models.SET_NULL)
    write_dt = models.DateTimeField(verbose_name='编制日期',
                                    blank=True, null=True)
    quota_clerk = models.ForeignKey(User, verbose_name='定额员',
                                    blank=True, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='process_lib_quota_clerk')
    quota_dt = models.DateTimeField(verbose_name='定额日期',
                                    blank=True, null=True)
    proofreader = models.ForeignKey(User, verbose_name='校对人',
                                    blank=True, null=True,
                                    related_name='process_lib_proofreader',
                                    on_delete=models.SET_NULL)
    proofread_dt = models.DateTimeField(verbose_name='校对日期',
                                        blank=True, null=True)
    statistician = models.ForeignKey(User, verbose_name='统计员',
                                     blank=True, null=True,
                                     related_name='process_lib_statistician',
                                     on_delete=models.SET_NULL)
    statistic_dt = models.DateTimeField(verbose_name='统计日期',
                                        blank=True, null=True)

    class Meta:
        verbose_name = '工艺库'
        verbose_name_plural = '工艺库'

    def __str__(self):
        return str(self.work_order)


class ProcessMaterial(models.Model):
    """
    工艺物料
    """
    lib = models.ForeignKey(ProcessLibrary, verbose_name='工艺库',
                            related_name='process_materials',
                            on_delete=models.CASCADE)
    ticket_number = models.IntegerField(verbose_name='票号')
    part_number = models.IntegerField(verbose_name='件号')
    drawing_number = models.CharField(verbose_name='图号', blank=True,
                                      default='', max_length=50)
    parent_drawing_number = models.CharField(verbose_name='所属图号',
                                             blank=True, default='',
                                             max_length=50)
    name = models.CharField(verbose_name='名称', blank=True,
                            default='', max_length=50)
    spec = models.CharField(verbose_name='规格', blank=True,
                            default='', max_length=20)
    count = models.IntegerField(verbose_name='数量')
    material = models.ForeignKey(Material, verbose_name='材质',
                                 blank=True, null=True,
                                 on_delete=models.PROTECT)
    name = models.CharField(verbose_name='名称', blank=True, max_length=50)
    piece_weight = models.FloatField(verbose_name='净重', blank=True, null=True)
    remark = models.CharField(verbose_name='备注', blank=True,
                              default='', max_length=50)

    class Meta:
        verbose_name = '工艺物料'
        verbose_name_plural = '工艺物料'

    def __str__(self):
        return self.name
