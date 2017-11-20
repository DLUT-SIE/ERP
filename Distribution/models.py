from django.db import models
from django.core.checks import Warning

from Core.models import Department
from Distribution import REVIEW_COMMENTS_CHOICES, REVIEW_COMMENTS_DEFAULT


class Product(models.Model):
    name = models.CharField(verbose_name='产品名称', max_length=50)
    approved = models.IntegerField(verbose_name='产品审核结果',
                                   choices=REVIEW_COMMENTS_CHOICES,
                                   default=REVIEW_COMMENTS_DEFAULT)
    terminated = models.BooleanField(verbose_name='终止状态', default=False)

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品"'

    def __str__(self):
        return self.name

    def getStatus(self):
        raise Warning('Deprecated: This will be removed soon, '
                      'use get_approved_display() instead')
        return self.get_approved_display()


class BidFile(models.Model):
    product = models.ForeignKey(Product, verbose_name='产品',
                                on_delete=models.CASCADE)
    src = models.ForeignKey(Department, verbose_name='来源部门',
                            related_name='bidfile_src',
                            on_delete=models.CASCADE)
    dst = models.ForeignKey(Department, verbose_name='接收部门',
                            related_name='bidfile_dst',
                            on_delete=models.CASCADE)
    name = models.CharField(verbose_name='名称', max_length=100)
    path = models.FileField(verbose_name='路径', upload_to='%Y/%m/%d')
    size = models.CharField(verbose_name='大小', max_length=50,
                            blank=True, null=True, default=None)
    upload_dt = models.DateTimeField(verbose_name='上传时间',
                                     null=True, blank=True, auto_now_add=True)
    approved = models.IntegerField(verbose_name='审核结果',
                                   choices=REVIEW_COMMENTS_CHOICES,
                                   default=REVIEW_COMMENTS_DEFAULT)

    class Meta:
        verbose_name = '招标文件'
        verbose_name_plural = '招标文件'

    def __str__(self):
        return self.name

    def getStatus(self):
        raise Warning('Deprecated: This will be removed soon, '
                      'use get_approved_display() instead')
        return self.get_approved_display()
