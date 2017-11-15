from django.db import models
from django.core.checks import Warning
from django.contrib.auth.models import User

from . import SELL_TYPES, MATERIAL_CATEGORY_CHOICES, GENDER_CHOICES


class WorkOrder(models.Model):
    identifier = models.CharField(verbose_name='编号',
                                  unique=True, max_length=20)
    sell_type = models.IntegerField(verbose_name='销售类型',
                                    choices=SELL_TYPES)
    client = models.CharField(verbose_name='客户名称', max_length=100)
    project = models.CharField(verbose_name='项目名称', max_length=100)
    product = models.CharField(verbose_name='产品名称', max_length=100)
    count = models.IntegerField(verbose_name='数量')
    finished = models.BooleanField(verbose_name='是否结束', default=False)

    class Meta:
        verbose_name = '工作令'
        verbose_name_plural = '工作令'

    def save(self, *args, **kwargs):
        super(WorkOrder, self).save(*args, **kwargs)
        # TODO: Only create SubWorkOrder on self create
        if self.subworkorder_set.all().count() > 0:
            return
        for index in range(self.count):
            name = '{}-{}'.format(self.identifier, index)
            sub_order = SubWorkOrder(order=self, index=index, name=name)
            sub_order.save()

    def suffix(self):
        return self.identifier[2:]

    def __str__(self):
        return self.identifier

    def getSellType(self):
        raise Warning('Deprecated: This will be removed soon, '
                      'use get_sell_type_display() instead')
        return self.get_sell_type_display


class SubWorkOrder(models.Model):
    work_order = models.ForeignKey(WorkOrder, verbose_name='所属工作令',
                                   on_delete=models.CASCADE)
    index = models.IntegerField(verbose_name='序号')
    name = models.CharField(verbose_name='工作令名', max_length=100)
    finished = models.BooleanField(verbose_name='是否结束', default=False)

    class Meta:
        verbose_name = "子工作令"
        verbose_name_plural = "子工作令"

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(verbose_name='材料名称', max_length=50)
    material_id = models.CharField(verbose_name='材料编号', blank=True,
                                   null=True, max_length=20)
    category = models.IntegerField(verbose_name='材料类别',
                                   blank=True, null=True,
                                   choices=MATERIAL_CATEGORY_CHOICES)

    class Meta:
        verbose_name = '材料'
        verbose_name_plural = '材料'

    def __str__(self):
        return self.name

    def display_material_name(self):
        raise Warning('Deprecated: This will be removed soon, '
                      'use get_category_display() instead')
        return "%s" % self.category


class Materiel(models.Model):
    work_order = models.ForeignKey(WorkOrder, verbose_name='所属工作令',
                              blank=True, null=True)
    index = models.CharField(verbose_name='票号', blank=True, max_length=20)
    sub_index = models.CharField(verbose_name='部件号', blank=True,
                                 null=True, max_length=20)
    schematic_index = models.CharField(verbose_name='图号', blank=True,
                                       null=True, max_length=50)
    parent_schematic_index = models.CharField(
        verbose_name='部件图号', blank=True, null=True, max_length=50)
    parent_name = models.CharField(
        verbose_name='部件名称', blank=True, null=True, max_length=100)
    material = models.ForeignKey(
        Material, verbose_name='材质', blank=True, null=True)
    name = models.CharField(verbose_name='名称', blank=True, max_length=100)
    count = models.CharField(verbose_name='数量', blank=True,
                             max_length=20, null=True)
    net_weight = models.FloatField(verbose_name='净重', blank=True, null=True)
    total_weight = models.FloatField(verbose_name='毛重', blank=True, null=True)
    quota = models.FloatField(verbose_name='定额', blank=True, null=True)
    quota_coefficient = models.FloatField(verbose_name='定额系数',
                                          blank=True, null=True)
    remark = models.CharField(verbose_name='备注', blank=True,
                              null=True, max_length=100)
    specification = models.CharField(verbose_name='规格', blank=True,
                                     null=True, max_length=20)
    standard = models.CharField(verbose_name='标准', blank=True,
                                null=True, max_length=20)
    unit = models.CharField(verbose_name='单位', blank=True,
                            null=True, max_length=20)
    status = models.CharField(verbose_name='状态', blank=True,
                              null=True, max_length=20)
    press = models.CharField(verbose_name='受压', blank=True,
                             null=True, max_length=20)
    recheck = models.CharField(verbose_name='复验', blank=True,
                               null=True, max_length=20)
    detection_level = models.CharField(verbose_name='探伤级别',
                                       blank=True, null=True, max_length=20)

    def total_weight_cal(self):
        if self.count and self.net_weight:
            return int(self.count) * self.net_weight

    def route(self):
        route_list = []
        for i in range(1, 11):
            step = getattr(self.circulationroute, "L%d" % i, None)
            if step is None:
                break
            route_list.append(step.get_name_display())
        return '.'.join(route_list)

    class Meta:
        verbose_name = '物料'
        verbose_name_plural = '物料'

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    user = models.OneToOneField(User, verbose_name='用户',
                                on_delete=models.CASCADE)
    phone = models.CharField(blank=True, null=True,
                             max_length=20, verbose_name='电话')
    mobile = models.CharField(blank=True, null=True,
                              max_length=20, verbose_name='移动电话')
    sex = models.IntegerField(blank=True, null=True,
                              choices=GENDER_CHOICES, verbose_name='性别')

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = '个人信息'

    def __str__(self):
        return self.user.first_name


class Department(models.Model):
    admin = models.ForeignKey(User, verbose_name='管理员', blank=True,
                              null=True, on_delete=models.SET_NULL)
    name = models.CharField(verbose_name='部门名', max_length=100)
    short_name = models.CharField(verbose_name='简写', max_length=50)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.name
