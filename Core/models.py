from django.db import models
from django.db import transaction
from django.core.checks import Warning
from django.contrib.auth.models import User

from Core import SELL_TYPES, MATERIAL_CATEGORY_CHOICES, GENDER_CHOICES


class WorkOrder(models.Model):
    """
    工作令

    Attributes
    ----------
    uid : CharField
        编号
    sell_type : IntegerField
        销售类型
    client : CharField
        客户名称
    project : CharField
        项目名称
    product : CharField
        产品名称
    count : IntegerField
        数量
    finished : BooleanField
        是否结束
    """
    uid = models.CharField(verbose_name='编号',
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
        created = False
        if not self.pk:
            created = True
        super(WorkOrder, self).save(*args, **kwargs)
        if created:
            with transaction.atomic():
                for index in range(1, 1 + self.count):
                    name = '{}-{}'.format(self.uid, index)
                    SubWorkOrder.objects.create(
                        work_order=self, index=index, name=name)

    def suffix(self):
        """
        获取部分uid信息

        note
        ----
        不赞成使用: 该函数将很快被移除，使用 `.uid` 代替

        Returns
        -------
        str
            部分uid信息
        """
        raise Warning('Deprecated: This will be removed soon, '
                      'use uid instead')
        return self.uid[2:]

    def __str__(self):
        return self.uid

    def getSellType(self):
        """
        获取销售类型

        note
        ----
        不赞成使用: 该函数将很快被移除，使用 `get_sell_type_display()` 代替

        Returns
        -------
        str
            销售类型
        """
        raise Warning('Deprecated: This will be removed soon, '
                      'use get_sell_type_display() instead')
        return self.get_sell_type_display()


class SubWorkOrder(models.Model):
    """
    子工作令, 在创建工作令时被自动创建

    Attributes
    ----------
    work_order : ForeignKey
        外键WorkOrder, 所属工作令
    index : IntegerField
        序号
    name : CharField
        工作令名
    finished : BooleanField
        是否结束
    """
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
    """
    材料

    注意与Materiel的拼写区别。

    Attributes
    ----------
    name : CharField
        材料名称
    material_id : CharField
        材料编号
    category : IntegerField
        材料类别
    """
    name = models.CharField(verbose_name='材料名称', max_length=50)
    # TODO: unique=True? Rename to uid?
    material_id = models.CharField(verbose_name='材料编号', blank=True,
                                   null=True, max_length=20)
    # TODO: Can be null?
    category = models.IntegerField(verbose_name='材料类别',
                                   blank=True, null=True,
                                   choices=MATERIAL_CATEGORY_CHOICES)

    class Meta:
        verbose_name = '材料'
        verbose_name_plural = '材料'

    def __str__(self):
        return self.name

    def display_material_name(self):
        """
        返回材料类别

        note
        ----
        不赞成使用: 该函数将很快被移除，使用 `get_category_display()` 代替

        Returns
        -------
        str
            材料类别
        """
        raise Warning('Deprecated: This will be removed soon, '
                      'use get_category_display() instead')
        return self.get_category_display()


class Materiel(models.Model):
    """
    物料

    注意与Material的拼写区别。

    Attributes
    ----------
    work_order : ForeignKey
        外键WorkOrder, 所属工作令
    index : CharField
        票号
    sub_index : CharField
        部件号
    schematic_index : CharField
        图号
    parent_schematic_index : CharField
        部件图号
    parent_name : CharField
        部件名称
    material : ForeignKey
        外键Material, 材质
    name : CharField
        名称
    count : CharField
        数量
    net_weight : FloatField
        净重
    total_weight : FloatField
        毛重
    quota : FloatField
        定额
    quota_coefficient : FloatField
        定额系数
    remark : CharField
        备注
    specification : CharField
        规格
    standard : CharField
        标准
    unit : CharField
        单位
    status : CharField
        状态
    press : CharField
        受压
    recheck : CharField
        复验
    detection_level : CharField
        探伤级别
    """
    # TODO: Rename attributes
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
    # TODO: IntegerField?
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
        """
        根据数量和净重返回总重量

        Returns
        -------
        float
            总重量
        """
        if self.count and self.net_weight:
            return int(self.count) * self.net_weight

    def route(self):
        """
        note
        ----
        使用情况未明
        """
        # TODO: Review
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
    """
    个人信息

    Attributes
    ----------
    user : OneToOneField
        一对一User, 用户
    phone : CharField
        电话
    mobile : CharField
        移动电话
    gender : IntegerField
        性别
    """
    user = models.OneToOneField(User, verbose_name='用户',
                                on_delete=models.CASCADE)
    phone = models.CharField(blank=True, null=True,
                             max_length=20, verbose_name='电话')
    mobile = models.CharField(blank=True, null=True,
                              max_length=20, verbose_name='移动电话')
    gender = models.IntegerField(blank=True, null=True,
                                 choices=GENDER_CHOICES, verbose_name='性别')

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = '个人信息'

    def __str__(self):
        return self.user.first_name


class Department(models.Model):
    """
    部门

    Attributes
    ----------
    admin : ForeignKey
        外键User, 管理员
    name : CharField
        部门名
    short_name : CharField
        简写
    """
    admin = models.ForeignKey(User, verbose_name='管理员',
                              blank=True, null=True,
                              on_delete=models.SET_NULL)
    name = models.CharField(verbose_name='部门名', max_length=100)
    short_name = models.CharField(verbose_name='简写', max_length=50)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.name
