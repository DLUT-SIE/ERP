from django.db import models

from Core.utils import gen_uuid
from Procurement import (BIDDING_SHEET_STATUS_CHOICES, COMMENT_STATUS_CHOICES,
                         IMPLEMENT_CLASS_CHOICES)


class BiddingSheet(models.Model):
    """
    标单
    """
    purchase_order = models.OneToOneField('PurchaseOrder',
                                          verbose_name='对应订购单',
                                          on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='标单编号', unique=True, max_length=20)
    # TODO: auto_now_add?
    create_dt = models.DateTimeField(verbose_name='创建时间',
                                     blank=True, null=True)
    status = models.IntegerField(verbose_name='标单状态', unique=True,
                                 choices=BIDDING_SHEET_STATUS_CHOICES)
    contract_number = models.CharField(verbose_name='合同编号', max_length=50,
                                       blank=True, default=gen_uuid)
    contract_amount = models.IntegerField(verbose_name='合同金额', default=0)
    billing_amount = models.IntegerField(verbose_name='开票金额', default=0)
    # TODO: Use choices?
    category = models.IntegerField(verbose_name='招标申请类型', default=0)

    class Meta:
        verbose_name = '标单'
        verbose_name_plural = '标单'

    def __str__(self):
        return self.uid


# TODO: Require all fields when necessary
class BiddingApplication(models.Model):
    """
    标单申请表
    """
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='标单申请编号', max_length=50,
                           unique=True)
    applicant = models.CharField(verbose_name='申请单位', max_length=40)
    requestor = models.CharField(verbose_name='需求单位', max_length=40)
    amount = models.IntegerField(verbose_name='数量', default=0)
    # TODO: ForeignKey?
    work_order = models.CharField(verbose_name='工作令', max_length=100,
                                  blank=True, null=True)
    plan_project = models.CharField(verbose_name='拟招(议)项目', max_length=40,
                                    blank=True, null=True)
    plan_dt = models.DateTimeField(verbose_name='拟招(议)标时间',
                                   blank=True, null=True)
    model = models.CharField(verbose_name='规格、型号', max_length=40,
                             null=True, blank=True)
    is_core_part = models.BooleanField(verbose_name='是否为核心件',
                                       default=False)
    category = models.CharField(verbose_name='项目类别', max_length=40,
                                null=True, blank=True)
    tender_dt = models.DateTimeField(verbose_name='招(议)标时间',
                                     null=True, blank=True)
    delivery_dt = models.DateTimeField(verbose_name='标书递送时间',
                                       null=True, blank=True)
    place = models.CharField(verbose_name='地点', max_length=40,
                             null=True, blank=True)
    status = models.IntegerField(verbose_name='状态',
                                 choices=COMMENT_STATUS_CHOICES)
    implement_class = models.IntegerField(verbose_name='实施类别',
                                          choices=IMPLEMENT_CLASS_CHOICES)

    class Meta:
        verbose_name = '标单申请表'
        verbose_name_plural = '标单申请表'

    def __str__(self):
        return str(self.bidding_sheet)


class ParityRatioCard(models.Model):
    """
    比质比价卡
    """
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    apply_id = models.CharField(verbose_name='标单申请编号', max_length=20)
    applicant = models.CharField(verbose_name='申请单位', max_length=40)
    requestor = models.CharField(verbose_name='需求单位', max_length=40)
    # TODO: ForeignKey?
    work_order = models.CharField(verbose_name='工作令', max_length=50,
                                  null=True, blank=True)
    amount = models.IntegerField(verbose_name='数量', null=True, blank=True)
    unit = models.CharField(verbose_name='单位', max_length=40,
                            blank=True, null=True)
    content = models.CharField(verbose_name='内容', max_length=40,
                               blank=True, null=True)
    material = models.CharField(verbose_name='材质', max_length=40,
                                blank=True, null=True)
    delivery_period = models.CharField(verbose_name='交货期', max_length=40,
                                       blank=True, null=True)
    status = models.IntegerField(verbose_name='状态',
                                 choices=COMMENT_STATUS_CHOICES)

    class Meta:
        verbose_name = '比质比价卡'
        verbose_name_plural = '比质比价卡'

    def __str__(self):
        return str(self.bidding_sheet)


class BiddingAcceptance(models.Model):
    """
    中标通知书
    """
    bidding_sheet = models.OneToOneField(BiddingSheet, verbose_name='标单',
                                         on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='标书编号', max_length=50, unique=True)
    # TODO: auto relate?
    requestor = models.CharField(verbose_name='招（议）标单位', max_length=40,
                                 blank=True, default='')
    content = models.CharField(verbose_name='招（议）标内容', max_length=40,
                               blank=True, default='')
    # TODO: IntegerField?
    amount = models.CharField(verbose_name='数量', null=True, max_length=40)
    accept_dt = models.DateTimeField(verbose_name='中标时间',
                                     null=True, blank=True)
    accept_money = models.CharField(verbose_name='中标金额', max_length=40,
                                    null=True, blank=True)
    accept_supplier = models.ForeignKey('Supplier', verbose_name='中标单位',
                                        null=True, blank=True,
                                        on_delete=models.SET_NULL)
    contact = models.CharField(verbose_name='联系人', max_length=40,
                               null=True, blank=True)
    contact_phone = models.CharField(verbose_name='联系电话', max_length=40,
                                     null=True, blank=True)

    class Meta:
        verbose_name = '中标通知书'
        verbose_name_plural = '中标通知书'

    def __str__(self):
        return '{}'.format(self.bidding_sheet.uid)
