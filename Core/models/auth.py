from django.db import models
from django.contrib.auth.models import User, Group

from Core import GENDER_CHOICES


class UserInfo(models.Model):
    """
    个人信息

    扩展Django的User对象的详细信息
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

    扩展Django的Group对象的功能
    """
    group = models.OneToOneField(Group, verbose_name='组',
                                 on_delete=models.CASCADE)
    superior = models.ForeignKey('self', verbose_name='上级部门',
                                 blank=True, null=True,
                                 on_delete=models.CASCADE)
    admin = models.ForeignKey(User, verbose_name='管理员',
                              blank=True, null=True,
                              on_delete=models.SET_NULL)
    short_name = models.CharField(verbose_name='简写', max_length=50)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.group.name
