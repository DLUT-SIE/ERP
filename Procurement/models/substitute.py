from django.db import models
from django.contrib.auth.models import User


class MaterialSubApply(models.Model):
    """
    材料代用申请单
    """
    uid = models.CharField(verbose_name='单据编号', max_length=30,
                           unique=True)
    figure_code = models.CharField(verbose_name='图号', max_length=30,
                                   blank=True, default='')
    # TODO: ForeignKey?
    work_order = models.CharField(verbose_name='工作令', max_length=30,
                                  blank=True, default='')
    # TODO: ForeignKey?
    production = models.CharField(verbose_name='产品名称', max_length=50,
                                  blank=True, default='')
    reason = models.CharField(verbose_name='代用原因和理由', max_length=200,
                              blank=True, default='')
    applicant = models.ForeignKey(User, verbose_name='申请人',
                                  null=True, blank=True,
                                  on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '材料代用申请单'
        verbose_name_plural = '材料代用申请单'

    def __str__(self):
        return self.uid


# TODO: Review this model
# TODO: Rename this model
class MaterialSubApplyItems(models.Model):
    """
    材料代用申请单明细
    """
    sub_apply = models.ForeignKey(MaterialSubApply,
                                  verbose_name='材料代用申请单',
                                  related_name='items',
                                  on_delete=models.CASCADE)
    part_figure_code = models.CharField(verbose_name='部件图号',
                                        max_length=100)
    # TODO: Duplicate with previous one?
    part_ticket_code = models.CharField(verbose_name='零件图号或票号',
                                        max_length=100)
    old_name = models.CharField(verbose_name='原材料名称',
                                max_length=100)
    old_standard = models.CharField(verbose_name='原材料标准',
                                    max_length=100)
    old_size = models.CharField(verbose_name='原材料规格和尺寸',
                                max_length=100)
    new_name = models.CharField(verbose_name='拟用材料名称', max_length=100)
    new_standard = models.CharField(verbose_name='拟用材料标准',
                                    max_length=100)
    new_size = models.CharField(verbose_name='拟用材料规格和尺寸',
                                max_length=100)

    class Meta:
        verbose_name = '材料代用申请单明细'
        verbose_name_plural = '材料代用申请单明细'

    def __str__(self):
        return '{}({})'.format(self.sub_apply, self.part_figure_code)
