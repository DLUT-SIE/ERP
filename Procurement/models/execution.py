from django.db import models
from django.contrib.auth.models import User

from Procurement import MATERIEL_TYPE_CHOICES


class MaterialExecution(models.Model):
    """
    材料执行表
    """
    uid = models.CharField(verbose_name='编号', max_length=50, unique=True)
    lister = models.ForeignKey(User, verbose_name='制表人',
                               on_delete=models.CASCADE)
    list_dt = models.DateTimeField(verbose_name='制表时间', auto_now_add=True)
    material_type = models.IntegerField(verbose_name='材料类型',
                                        choices=MATERIEL_TYPE_CHOICES)
    process_requirement = models.CharField(verbose_name='工艺需求',
                                           max_length=200,
                                           blank=True, default='')

    class Meta:
        verbose_name = '材料执行表'
        verbose_name_plural = '材料执行表'

    def __str__(self):
        return self.uid


class MaterialExecutionDetail(models.Model):
    """
    材料执行表明细
    """
    material_execution = models.ForeignKey(MaterialExecution,
                                           verbose_name='材料执行表',
                                           null=True, blank=True,
                                           related_name='materialexecution',
                                           on_delete=models.SET_NULL)
    material = models.ForeignKey('ProcurementMaterial', verbose_name='物料',
                                 related_name='material',
                                 on_delete=models.CASCADE)
    batch_number = models.CharField(verbose_name='出厂批号', max_length=50,
                                    null=True, blank=True)
    quota = models.CharField(verbose_name='定额', max_length=50,
                             null=True, blank=True)
    part = models.CharField(verbose_name='零件', max_length=50,
                            null=True, blank=True)
    oddments = models.CharField(verbose_name='余料', max_length=50,
                                null=True, blank=True)
    remark = models.CharField(verbose_name='备注', max_length=200,
                              null=True, blank=True)

    class Meta:
        verbose_name = '材料执行表明细'
        verbose_name_plural = '材料执行表明细'

    def __str__(self):
        return '{}-{}'.format(self.material_execution, self.materiel)
