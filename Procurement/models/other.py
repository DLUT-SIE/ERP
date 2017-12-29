from django.db import models
from django.contrib.auth.models import User

from Core.utils import DynamicHashPath
from Procurement import (BIDDING_SHEET_STATUS_CHOICES, INVENTORY_TYPE,
                         INVENTORY_TYPE_NOTSET)


class ArrivalInspection(models.Model):
    """
    到货检验
    """
    material = models.OneToOneField('ProcurementMaterial', verbose_name='材料')
    material_confirm = models.BooleanField(verbose_name='实物确认',
                                           default=False)
    soft_confirm = models.BooleanField(verbose_name='软件确认',
                                       default=False)
    inspection_confirm = models.BooleanField(verbose_name='检验通过',
                                             default=False)
    passed = models.BooleanField(verbose_name='是否通过', default=False)

    class Meta:
        verbose_name = '到货检验'
        verbose_name_plural = '到货检验'

    def __str__(self):
        return str(self.material)

    # 生成入库单，成功后回调。
    def entry_confirm(self):
        self.passed = True
        self.save()


class ProcessFollowingInfo(models.Model):
    """
    过程跟踪记录
    """
    bidding_sheet = models.ForeignKey('BiddingSheet', verbose_name='标单',
                                      on_delete=models.CASCADE)
    following_dt = models.DateTimeField(verbose_name='跟踪时间')
    following_method = models.CharField(verbose_name='跟踪方式', max_length=20)
    following_feedback = models.CharField(verbose_name='跟踪反馈',
                                          max_length=200)
    path = models.FileField(verbose_name='路径',
                            upload_to=DynamicHashPath('ProcessFollowingInfo'))
    executor = models.ForeignKey(User, verbose_name='执行人',
                                 on_delete=models.CASCADE)
    inform_process = models.BooleanField(verbose_name='是否通知工艺',
                                         default=False)

    class Meta:
        verbose_name = '过程跟踪记录'
        verbose_name_plural = '过程跟踪记录'

    def __str__(self):
        return self.bidding_sheet.uid


# TODO: Rename this model
class StatusChange(models.Model):
    """
    状态更改记录
    """
    bidding_sheet = models.ForeignKey('BiddingSheet', verbose_name='标单',
                                      on_delete=models.CASCADE)
    original_status = models.IntegerField(verbose_name='标单状态', unique=True,
                                          choices=BIDDING_SHEET_STATUS_CHOICES)
    new_status = models.IntegerField(verbose_name='标单状态', unique=True,
                                     choices=BIDDING_SHEET_STATUS_CHOICES)
    change_user = models.ForeignKey(User, verbose_name='更改用户',
                                    on_delete=models.CASCADE)
    change_dt = models.DateTimeField(verbose_name='更改时间',
                                     auto_now_add=True)
    normal_change = models.BooleanField(verbose_name='是否正常更改',
                                        default=True)
    reason = models.CharField(verbose_name='回溯原因',
                              max_length=200, blank=True, default='')

    class Meta:
        verbose_name = '状态更改记录'
        verbose_name_plural = '状态更改记录'

    def __str__(self):
        return '{}({} -> {})'.format(self.bidding_sheet,
                                     self.get_original_status_display(),
                                     self.get_new_status_display())


class Quotation(models.Model):
    """
    报价单
    """
    inventory_type = models.IntegerField(verbose_name='明细类型',
                                         choices=INVENTORY_TYPE,
                                         default=INVENTORY_TYPE_NOTSET)
    name_spec = models.CharField(verbose_name='规格及名称', max_length=50,
                                 blank=True, null=True)
    material_mark = models.CharField(verbose_name='材质或牌号', max_length=50,
                                     blank=True, null=True)
    unit_price = models.CharField(verbose_name='单价', max_length=50,
                                  blank=True, null=True)
    unit = models.CharField(verbose_name='单位', max_length=50,
                            blank=True, null=True)
    supplier = models.ForeignKey('Supplier', verbose_name='供应商',
                                 on_delete=models.CASCADE,
                                 related_name='quotations')

    class Meta:
        verbose_name = '报价单'
        verbose_name_plural = '报价单'

    def __str__(self):
        return '{}-{}:{}({})'.format(self.name_spec, self.material_mark,
                                     self.supplier, self.unit_price)
