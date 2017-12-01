from django.db import models

from Core.models import Department
from Core.utils import DynamicHashPath
from Distribution import REVIEW_STATUS_CHOICES, REVIEW_STATUS_DEFAULT


class Product(models.Model):
    """
    产品

    用以表示一个产品的基本信息
    """
    name = models.CharField(verbose_name='名称', max_length=50)
    terminated = models.BooleanField(verbose_name='终止状态', default=False)
    status = models.IntegerField(verbose_name='状态',
                                 choices=REVIEW_STATUS_CHOICES,
                                 default=REVIEW_STATUS_DEFAULT)

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品"'

    def __str__(self):
        return self.name


class BiddingDocument(models.Model):
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
                                     null=True, blank=True, auto_now_add=True)
    status = models.IntegerField(verbose_name='状态',
                                 choices=REVIEW_STATUS_CHOICES,
                                 default=REVIEW_STATUS_DEFAULT)

    class Meta:
        verbose_name = '产品招标文件'
        verbose_name_plural = '产品招标文件'

    def __str__(self):
        return self.path.name
