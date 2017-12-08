from django.db import models

from Core.models import Department
from Core.utils import DynamicHashPath, transition
from Core.utils.fsm import TransitionMeta
from Distribution import (REVIEW_STATUS_CHOICES, REVIEW_STATUS_DEFAULT,
                          REVIEW_STATUS_PASS, REVIEW_STATUS_FAIL)


class Product(models.Model, metaclass=TransitionMeta):
    """
    产品

    用以表示一个产品的基本信息
    """
    name = models.CharField(verbose_name='名称', max_length=50)
    terminated = models.BooleanField(verbose_name='终止状态', default=False)
    status = models.IntegerField(verbose_name='状态',
                                 choices=REVIEW_STATUS_CHOICES,
                                 default=REVIEW_STATUS_DEFAULT)

    @transition(field='status',
                source=(REVIEW_STATUS_DEFAULT, REVIEW_STATUS_FAIL),
                target=REVIEW_STATUS_PASS, name='pass')
    def review_pass(self, request):
        """
        产品审核通过
        """
        pass

    @transition(field='status', source=REVIEW_STATUS_DEFAULT,
                target=REVIEW_STATUS_FAIL, name='fail')
    def review_fail(self, request):
        """
        产品审核不通过
        """
        pass

    @transition(field='terminated', source=False, target=True)
    def terminate(self, request):
        """
        产品终止
        """
        pass

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品"'

    def __str__(self):
        return self.name


class BiddingDocument(models.Model, metaclass=TransitionMeta):
    """
    产品招标文件

    经销管理部门与生产科、工艺科、采购科之间交流的招标文件
    """
    product = models.ForeignKey(Product, verbose_name='对应产品',
                                related_name='documents',
                                on_delete=models.CASCADE)
    src = models.ForeignKey(Department, verbose_name='来源部门',
                            related_name='bidding_doc_src',
                            on_delete=models.CASCADE)
    dst = models.ForeignKey(Department, verbose_name='接收部门',
                            related_name='bidding_doc_dst',
                            on_delete=models.CASCADE)
    path = models.FileField(verbose_name='路径',
                            upload_to=DynamicHashPath('BiddingDocument'))
    upload_dt = models.DateTimeField(verbose_name='上传时间',
                                     auto_now_add=True)
    status = models.IntegerField(verbose_name='状态',
                                 choices=REVIEW_STATUS_CHOICES,
                                 default=REVIEW_STATUS_DEFAULT)

    @transition(field='status',
                source=(REVIEW_STATUS_DEFAULT, REVIEW_STATUS_FAIL),
                target=REVIEW_STATUS_PASS, name='pass')
    def review_pass(self, request):
        """
        招标文件审核通过
        """
        pass

    @transition(field='status', source=REVIEW_STATUS_DEFAULT,
                target=REVIEW_STATUS_FAIL, name='fail')
    def review_fail(self, request):
        """
        招标文件审核不通过
        """
        pass

    @transition(field='status', source=REVIEW_STATUS_FAIL,
                target=REVIEW_STATUS_DEFAULT, name='reset')
    def review_reset(self, request):
        """
        招标文件审核状态重置
        """
        pass

    class Meta:
        verbose_name = '产品招标文件'
        verbose_name_plural = '产品招标文件'

    def __str__(self):
        return self.path.name
