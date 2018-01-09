from django.db import models

from Core.utils import DynamicHashPath
from Procurement import COMMENT_STATUS_CHOICES, SUPPLIER_REL_C_CHOICES
from Core.utils.fsm import transition, TransitionMeta
from Procurement import (
    COMMENT_STATUS_CHECK_FILL,
    COMMENT_STATUS_CHECK_OPERATOR_COMMENT,
    COMMENT_STATUS_CHECK_LEAD_COMMENT,
    COMMENT_STATUS_CHECK_QUALITY_COMMENT,
    COMMENT_STATUS_CHECK_ECONOMIC_COMMENT,
    COMMENT_STATUS_CHECK_COMPREHENSIVE_COMMENT,
    )


class Supplier(models.Model):
    """
    供应商
    """
    uid = models.CharField(verbose_name='供应商编号', max_length=20,
                           unique=True)
    name = models.CharField(verbose_name='供应商名称', max_length=50)
    bidding_sheets = models.ManyToManyField('BiddingSheet',
                                            verbose_name='参与标单',
                                            through='SupplyRelationship')

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = '供应商'

    def __str__(self):
        return self.name


class SupplierCheck(models.Model, metaclass=TransitionMeta):
    """
    供应商审核
    """
    bidding_sheet = models.OneToOneField('BiddingSheet', verbose_name='标单',
                                         on_delete=models.CASCADE)
    # TODO: ForeignKey?
    applicant = models.CharField(verbose_name='申请单位', max_length=40)
    application_dt = models.DateTimeField(verbose_name='申请时间')
    project = models.CharField(verbose_name='项目名称', max_length=40)
    estimated_price = models.FloatField(verbose_name='估算价格')
    basic_situation = models.CharField(verbose_name='招（议）标项目基本情况',
                                       max_length=100,
                                       blank=True, default='')
    status = models.IntegerField(verbose_name='状态',
                                 choices=COMMENT_STATUS_CHOICES)

    class Meta:
        verbose_name = '供应商审核'
        verbose_name_plural = '供应商审核'

    def __str__(self):
        return str(self.bidding_sheet)

    @transition(
        field='status', source=COMMENT_STATUS_CHECK_FILL,
        target=COMMENT_STATUS_CHECK_OPERATOR_COMMENT)
    def operator_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_CHECK_OPERATOR_COMMENT,
        target=COMMENT_STATUS_CHECK_LEAD_COMMENT)
    def lead_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_CHECK_LEAD_COMMENT,
        target=COMMENT_STATUS_CHECK_QUALITY_COMMENT)
    def quality_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_CHECK_QUALITY_COMMENT,
        target=COMMENT_STATUS_CHECK_ECONOMIC_COMMENT)
    def economic_comment():
        # TODO
        pass

    @transition(
        field='status', source=COMMENT_STATUS_CHECK_ECONOMIC_COMMENT,
        target=COMMENT_STATUS_CHECK_COMPREHENSIVE_COMMENT)
    def comprehensive_comment():
        # TODO
        pass


class SupplierDocument(models.Model):
    """
    供应商文件
    """
    supplier = models.ForeignKey(Supplier, verbose_name='供应商',
                                 on_delete=models.CASCADE, related_name='docs')
    path = models.FileField(verbose_name='路径',
                            upload_to=DynamicHashPath('SupplierDocument'))
    upload_dt = models.DateTimeField(verbose_name='上传时间',
                                     auto_now_add=True)

    class Meta:
        verbose_name = '供应商文件'
        verbose_name_plural = '供应商文件'

    def __str__(self):
        return self.path.name


class SupplyRelationship(models.Model):
    """
    标单供应关系
    """
    bidding_sheet = models.ForeignKey('BiddingSheet', verbose_name='标单',
                                      on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, verbose_name='供应商',
                                 on_delete=models.CASCADE)
    # TODO: what are these fields?
    A = models.BooleanField(verbose_name='A', blank=True, default=False)
    B = models.BooleanField(verbose_name='B', blank=True, default=False)
    C = models.IntegerField(verbose_name='C', choices=SUPPLIER_REL_C_CHOICES)
    D = models.BooleanField(verbose_name='D', blank=True, default=False)
    E = models.BooleanField(verbose_name='E', blank=True, default=False)
    F = models.BooleanField(verbose_name='F', blank=True, default=False)
    G = models.BooleanField(verbose_name='G', blank=True, default=False)
    scope = models.CharField(verbose_name='认定业务范围', max_length=40,
                             blank=True, default='')
    supplier_code = models.CharField(verbose_name='供方代码', max_length=40,
                                     blank=True, default='')
    price = models.FloatField(verbose_name='价格')
    status = models.CharField(verbose_name='厂家协作能力质量情况及业绩',
                              max_length=100, blank=True, default='')
    delivery_payment = models.CharField(verbose_name='交货及支付条件',
                                        max_length=40, blank=True, default='')

    class Meta:
        verbose_name = '标单供应关系'
        verbose_name_plural = '标单供应关系'

    def __str__(self):
        return '{} - {}'.format(self.bidding_sheet, self.supplier)
