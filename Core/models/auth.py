from django.db import models
from django.contrib.auth.models import User, Group

from Core import GENDER_CHOICES, GENDER_MALE


class UserInfo(models.Model):
    """
    个人信息

    扩展Django的User对象的详细信息
    """
    user = models.OneToOneField(User, verbose_name='用户',
                                related_name='info',
                                editable=False,
                                on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='电话', max_length=20,
                             blank=True, default='')
    mobile = models.CharField(verbose_name='移动电话', max_length=20,
                              blank=True, default='')
    gender = models.IntegerField(verbose_name='性别', choices=GENDER_CHOICES,
                                 default=GENDER_MALE)

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = '个人信息'

    def __str__(self):
        return '{1}(用户名:{0})'.format(
            self.user.username, self.user.first_name)


class DistributionDepartmentManager(models.Manager):
    def get_queryset(self):
        # TODO: To real
        return super().get_queryset().filter(id=1)


class ProcessDepartmentManager(models.Manager):
    def get_queryset(self):
        # TODO: To real
        return super().get_queryset().filter(id=2)


class ProcurementDepartmentManager(models.Manager):
    def get_queryset(self):
        # TODO: To real
        return super().get_queryset().filter(id=3)


class ProductionDepartmentManager(models.Manager):
    def get_queryset(self):
        # TODO: To real
        return super().get_queryset().filter(id=4)


class Department(models.Model):
    """
    部门

    扩展Django的Group对象的功能
    """
    group = models.OneToOneField(Group, verbose_name='组',
                                 on_delete=models.CASCADE)
    superior = models.ForeignKey('self', verbose_name='上级部门',
                                 blank=True, null=True,
                                 on_delete=models.CASCADE)
    admin = models.ForeignKey(User, verbose_name='部门管理员',
                              blank=True, null=True,
                              on_delete=models.SET_NULL)
    short_name = models.CharField(verbose_name='简写', max_length=50)

    # Custom managers
    objects = models.Manager()
    distribution = DistributionDepartmentManager()
    process = ProcessDepartmentManager()
    procurement = ProcurementDepartmentManager()
    production = ProductionDepartmentManager()

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.group.name

    @classmethod
    def get_departments_dict(cls):
        departments = {d.group.name: d.id for d in cls.objects.all()}
        return departments
