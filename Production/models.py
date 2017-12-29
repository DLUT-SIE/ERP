from django.db import models
from django.contrib.auth.models import User

from Core.models import WorkOrder, SubWorkOrder, UserInfo
from Process import PROCESS_CHOICES
from Process.models import ProcessMaterial, ProcessStep
from Production import (PRODUCTION_PLAN_STATUS_CHOICES,
                        PRODUCTION_PLAN_RELAX)


# TODO: Review model name
class SubMaterial(models.Model):
    """
    子工作票
    """
    material = models.ForeignKey(ProcessMaterial, verbose_name='工艺物料',
                                 on_delete=models.CASCADE)
    sub_order = models.ForeignKey(SubWorkOrder, verbose_name='子工作令',
                                  on_delete=models.CASCADE)
    estimated_finish_dt = models.DateTimeField(verbose_name='计划完成日期',
                                               blank=True, null=True)
    actual_finish_dt = models.DateTimeField(verbose_name='实际完成日期',
                                            blank=True, null=True)

    class Meta:
        verbose_name = '子工作票'
        verbose_name_plural = '子工作票'

    def __str__(self):
        return '{} {}'.format(self.sub_order, self.material)


class ProductionWorkGroup(models.Model):
    """
    生产工作组
    """
    name = models.CharField(verbose_name='名字', max_length=20)
    process = models.IntegerField(verbose_name='工序',
                                  choices=PROCESS_CHOICES)

    class Meta:
        verbose_name = '生产工作组'
        verbose_name_plural = '生产工作组'

    def __str__(self):
        return self.name


class ProductionUser(models.Model):
    """
    生产人员
    """
    user_info = models.OneToOneField(UserInfo, verbose_name='详细信息',
                                     on_delete=models.CASCADE)
    work_group = models.ForeignKey(ProductionWorkGroup,
                                   verbose_name='生产工作组',
                                   blank=True, null=True,
                                   on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '生产人员'
        verbose_name_plural = '生产人员'

    def __str__(self):
        return str(self.user_info)


class ProcessDetail(models.Model):
    """
    工序详细信息
    """
    sub_material = models.ForeignKey(SubMaterial, verbose_name='子工作票',
                                     on_delete=models.CASCADE)
    process_step = models.OneToOneField(ProcessStep, verbose_name='工序步骤',
                                        on_delete=models.CASCADE)
    work_group = models.ForeignKey(ProductionWorkGroup, verbose_name='工作组',
                                   blank=True, null=True,
                                   on_delete=models.SET_NULL)
    # *IMPORTANT*
    # TODO: estimated should be changed if 'Plan' is noun and not verb
    estimated_start_dt = models.DateTimeField(verbose_name='计划开始日期',
                                              blank=True, null=True)
    estimated_finish_dt = models.DateTimeField(verbose_name='计划完成日期',
                                               blank=True, null=True)
    actual_finish_dt = models.DateTimeField(verbose_name='实际完成日期',
                                            blank=True, null=True)
    # plan_startdate = models.DateTimeField(
    #     blank = True, null= True, verbose_name = u"计划开始时间")
    # plan_enddate = models.DateTimeField(
    #     blank = True, null= True, verbose_name = u"计划完成时间")
    # complete_process_date = models.DateTimeField(
    #     blank = True, null= True, verbose_name = u"完成时间")

    inspector = models.ForeignKey(User, verbose_name='检查者',
                                  blank=True, null=True,
                                  on_delete=models.SET_NULL)
    inspection_dt = models.DateTimeField(verbose_name='检查时间',
                                         blank=True, null=True)
    remark = models.CharField(verbose_name='检查内容', max_length=200,
                              blank=True, default='')

    class Meta:
        verbose_name = '工序详细信息'
        verbose_name_plural = '工序详细信息'
        # TODO: Review this unique setting
        unique_together = ('sub_material', 'process_step')

    def __str__(self):
        return '{}({})'.format(self.sub_material, self.process_step)


class ComprehensiveDepartmentFileList(models.Model):
    """
    综合工部文件清单检查
    """
    sub_order = models.ForeignKey(SubWorkOrder, verbose_name='工作令',
                                  on_delete=models.CASCADE)
    sketch = models.BooleanField(verbose_name='简图', default=False)
    pressure_test = models.BooleanField(verbose_name='试压工艺', default=False)
    process_lib = models.BooleanField(verbose_name='工艺库', default=False)
    product_graph = models.BooleanField(verbose_name='产品图', default=False)
    encasement_graph = models.BooleanField(verbose_name='装箱图',
                                           default=False)
    shipping_mark = models.BooleanField(verbose_name='唛头', default=False)
    encasement_list = models.BooleanField(verbose_name='装箱单', default=False)
    coating_detail = models.BooleanField(verbose_name='涂装明细',
                                         default=False)

    class Meta:
        verbose_name = '综合工部文件清单检查'
        verbose_name_plural = '综合工部文件清单检查'

    def __str__(self):
        return str(self.sub_order)


class ProductionPlan(models.Model):
    """
    生产计划
    """
    work_order = models.ForeignKey(WorkOrder, verbose_name='工作令',
                                   on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='生产计划状态',
                                 choices=PRODUCTION_PLAN_STATUS_CHOICES,
                                 default=PRODUCTION_PLAN_RELAX)
    plan_dt = models.DateTimeField(verbose_name='计划年月')
    remark = models.CharField(verbose_name='备注', blank=True,
                              default='', max_length=50)

    class Meta:
        verbose_name = '生产计划'
        verbose_name_plural = '生产计划'

    def __str__(self):
        return str(self.work_order)
