from django.db import models

from Core.utils import DynamicHashPath
from Procurement.models import MaterialExecutionDetail
from Process.models import ProcessMaterial


class ProcessReview(models.Model):
    """
    工艺性审查表
    """
    process_material = models.ForeignKey(ProcessMaterial,
                                         verbose_name='零件',
                                         on_delete=models.CASCADE)
    problem = models.CharField(verbose_name='存在问题', max_length=200,
                               blank=True, default='')
    advice = models.CharField(verbose_name='改进建议', max_length=200,
                              blank=True, default='')

    class Meta:
        verbose_name = '工艺性审查表'
        verbose_name_plural = '工艺性审查表'

    def __str__(self):
        return str(self.process_material)


class ProgrammingBlankingChart(models.Model):
    """
    编程套料图
    """
    execution_detail = models.ForeignKey(MaterialExecutionDetail,
                                         verbose_name='材料执行表详细情况',
                                         on_delete=models.CASCADE)
    path = models.FileField(
        verbose_name='路径',
        upload_to=DynamicHashPath('ProgrammingBlankingChart'))
    upload_dt = models.DateTimeField(verbose_name='上传时间',
                                     auto_now_add=True)

    class Meta:
        verbose_name = '编程套料图'
        verbose_name_plural = '编程套料图'

    def __str__(self):
        return self.path.name
