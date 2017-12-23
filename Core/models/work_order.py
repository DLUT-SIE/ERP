from django.db import models, transaction

from Core import SELL_TYPES
from Distribution.models import Product


class WorkOrder(models.Model):
    """
    工作令

    用以追踪一个产品合同的相关情况(工艺、采购、库存、生产)
    """
    uid = models.CharField(verbose_name='编号',
                           unique=True, max_length=20)
    sell_type = models.IntegerField(verbose_name='销售类型',
                                    choices=SELL_TYPES)
    client = models.CharField(verbose_name='客户名称', max_length=100)
    project = models.CharField(verbose_name='项目名称', max_length=100)
    product = models.OneToOneField(Product, verbose_name='产品',
                                   on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='数量')
    finished = models.BooleanField(verbose_name='已结束', default=False)

    class Meta:
        verbose_name = '工作令'
        verbose_name_plural = '工作令'

    def save(self, *args, **kwargs):
        """
        工作令保存

        工作令首次保存时会根据 *count* 自动创建子工作令
        """
        created = False
        if not self.pk:
            created = True
        with transaction.atomic():
            super(WorkOrder, self).save(*args, **kwargs)
            if created:
                sub_orders = []
                for index in range(1, 1 + self.count):
                    sub_orders.append(SubWorkOrder(work_order=self,
                                                   index=index))
                SubWorkOrder.objects.bulk_create(sub_orders)

    def __str__(self):
        return self.uid


class SubWorkOrder(models.Model):
    """
    子工作令

    在创建工作令时被自动创建, 用以追踪对应工作令产品的其中一个产品
    """
    work_order = models.ForeignKey(WorkOrder, verbose_name='所属工作令',
                                   on_delete=models.CASCADE)
    index = models.IntegerField(verbose_name='序号')
    finished = models.BooleanField(verbose_name='已结束', default=False)

    class Meta:
        verbose_name = "子工作令"
        verbose_name_plural = "子工作令"

    @property
    def uid(self):
        return '{}-{}'.format(self.work_order, self.index)

    def __str__(self):
        return self.uid
