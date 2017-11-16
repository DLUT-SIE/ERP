from django.db import models
from django.contrib.auth.models import User

from Core.models import WorkOrder, Materiel, SubWorkOrder, UserInfo
from Core.utils import gen_uuid
from Process import PROCESS_CHOICES
from Production import (PRODUCTION_PLAN_STATUS_CHOICES,
                        PRODUCTION_PLAN_RELAX)


class SubMateriel(models.Model):
    # TODO: What's 工作票?
    materiel = models.ForeignKey(Materiel, verbose_name='工作票',
                                 on_delete=models.CASCADE)
    sub_order = models.ForeignKey(SubWorkOrder, verbose_name='所属工作令',
                                  on_delete=models.CASCADE)
    estimated_finish_date = models.DateField(verbose_name='计划完成日期',
                                             blank=True, null=True)
    actual_finish_date = models.DateField(verbose_name='实际完成日期',
                                          blank=True, null=True)

    class Meta:
        verbose_name = '子工作票'
        verbose_name_plural = '子工作票'

    def __str__(self):
        return '{} {}'.format(self.sub_order.name, self.materiel.index)


class ProductionWorkGroup(models.Model):
    name = models.CharField(verbose_name='名字', max_length=20)
    process = models.IntegerField(verbose_name='工序',
                                  choices=PROCESS_CHOICES)

    class Meta:
        verbose_name = '生产工作组'
        verbose_name_plural = '生产工作组'

    def __str__(self):
        return self.name


class ProductionUser(models.Model):
    user_info = models.OneToOneField(UserInfo, verbose_name='生产人员',
                                     on_delete=models.CASCADE)
    # TODO: Is this necessary?
    work_group = models.ForeignKey(ProductionWorkGroup,
                                   verbose_name='所属工作组',
                                   blank=True, null=True,
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = '生产人员'
        verbose_name_plural = '生产人员'

    def __unicode__(self):
        return '%s' % (self.production_user_id.name)


# TODO: Duplicate with ProcessRoute and ProcessStep?
class ProcessDetail(models.Model):
    sub_materiel = models.ForeignKey(SubMateriel, verbose_name='工作票',
                                     on_delete=models.CASCADE)
    process = models.IntegerField(verbose_name='工序',
                                  choices=PROCESS_CHOICES)
    process_order = models.IntegerField(verbose_name='工序序号')
    man_hours = models.CharField(verbose_name='工时', max_length=20,
                                 blank=True, null=True,)
    work_group = models.ForeignKey(ProductionWorkGroup, verbose_name='工作组',
                                   blank=True, null=True,
                                   on_delete=models.CASCADE)
    # *IMPORTANT*
    # TODO: estimated should be changed if 'Plan' is noun and not verb
    estimated_start_date = models.DateField(verbose_name='计划开始日期',
                                            blank=True, null=True)
    estimated_finish_date = models.DateField(verbose_name='计划完成日期',
                                             blank=True, null=True)
    actual_finish_date = models.DateField(verbose_name='实际完成日期',
                                          blank=True, null=True)
    # plan_startdate = models.DateField(
    #     blank = True, null= True, verbose_name = u"计划开始时间")
    # plan_enddate = models.DateField(
    #     blank = True, null= True, verbose_name = u"计划完成时间")
    # complete_process_date = models.DateField(
    #     blank = True, null= True, verbose_name = u"完成时间")

    inspector = models.ForeignKey(User, verbose_name='检查者', null=True)
    inspection_date = models.DateField(verbose_name='检查时间',
                                       blank=True, null=True)
    inspection_content = models.CharField(verbose_name='检查内容',
                                          max_length=500,
                                          blank=True, null=True)

    class Meta:
        verbose_name = '工序详细信息'
        verbose_name_plural = '工序详细信息'
        unique_together = ('sub_materiel', 'process_order')

    def __str__(self):
        return '{}-{}-{}'.format(self.sub_materiel,
                                 self.process_order,
                                 self.process)


class ComprehensiveDepartmentFileList(models.Model):
    sub_order = models.ForeignKey(SubWorkOrder, verbose_name='工作令',
                                  on_delete=models.CASCADE)
    sketch = models.BooleanField(verbose_name='简图', default=False)
    pressure_test = models.BooleanField(verbose_name='试压工艺', default=False)
    process_lib = models.BooleanField(verbose_name='工艺库', default=False)
    product_graph = models.BooleanField(verbose_name='产品图', default=False)
    encasement_graph = models.BooleanField(verbose_name='装箱图', default=False)
    shipping_mark = models.BooleanField(verbose_name='唛头', default=False)
    encasement_list = models.BooleanField(verbose_name='装箱单', default=False)
    coating_detail = models.BooleanField(verbose_name='涂装明细', default=False)

    class Meta:
        verbose_name = '综合工部文件清单'
        verbose_name_plural = '综合工部文件清单'

    def __str__(self):
        return str(self.sub_order)


class ProductionPlan(models.Model):
    work_order = models.ForeignKey(WorkOrder, verbose_name='工作令',
                                   on_delete=models.CASCADE)
    identifier = models.CharField(verbose_name='生产计划编号',
                                  max_length=50, default=gen_uuid)
    status = models.IntegerField(verbose_name='生产计划状态',
                                 choices=PRODUCTION_PLAN_STATUS_CHOICES,
                                 default=PRODUCTION_PLAN_RELAX)
    plan_date = models.DateField(verbose_name='计划年月', auto_now_add=True)

    class Meta:
        verbose_name = '生产计划'
        verbose_name_plural = '生产计划'

    def __str__(self):
        return self.identifier
