from functools import wraps
from collections import Iterable

from django.db import transaction
from django.core import exceptions


class Transition:
    """
    用于控制工作流状态转移的方法装饰器

    :用途:
        - 状态更新
        - 状态回退

    :特点:
        原子性


    Parameters
    ------------
    field
        进行状态转移的字段
    source
        起始状态, 使用'*'表示任意状态
    target
        目标状态, 完成对应操作后转入状态
    conditions
        进行该状态转移所需的额外条件, 默认跳过该检查, 若为'bool'类型, 则在检查\
    时直接返回该值, 若为函数, 则在检查时接收一个参数'request'并返回其调用结果,\
    否则不允许操作
    permission
        进行该状态转移所需的权限, 默认跳过该检查, 若为'bool'类型，则在检查时直\
    接返回该值, 若为'str'类型, 则根据'user.has_perm'进行判断, 若为函数, 则在检\
    查时接收一个参数'request'并返回其调用结果, 否则不允许操作

    Example
    ---------
    .. code:: python

        from Core.utils import Transition


        class Example(models.Model):
            status = models.IntegerField(verbose_name='状态',
                                         choices=REVIEW_STATUS_CHOICES,
                                         default=REVIEW_STATUS_DEFAULT)

            @Transition(field=status, source='*', target=REVIEW_STATUS_PASS)
            def review_pass(self, request):
                # Do some relavent actions
                # status will be updated and saved automatically
                pass

    Raises
    -------
    PermissionDenied
        当操作权限检查失败后抛出
    ValidationError
        当前置状态或额外条件检查失败后抛出


    :适用对象:
        模型方法

    :作者:
        杜佑宸 <youchen.du@gmail.com>

    """
    def __init__(self, field, source, target,
                 conditions=None, permission=None):
        self.field = field
        self.source = source
        self.target = target
        self.conditions = conditions
        self.permission = permission

    def _has_perm(self, inst, request):
        """
        检查操作权限
        """
        if self.permission is None:
            return True
        elif isinstance(self.permission, bool):
            return self.permission
        elif isinstance(self.permission, str):
            return request.user.has_perm(self.permission)
        elif callable(self.permission):
            return self.permission(inst, request)
        else:
            return False

    def _can_trans(self, request):
        """
        检查前置状态
        """
        if self.source == self.field or self.source == '*':
            return True
        elif (not isinstance(self.source, str) and
                isinstance(self.source, Iterable)):
            return self.field in self.source
        else:
            return False

    def _match_conds(self, inst, request):
        """
        检查额外条件
        """
        if self.conditions is None:
            return True
        elif isinstance(self.conditions, bool):
            return self.conditions
        elif callable(self.conditions):
            return self.conditions(inst, request)
        else:
            return False

    def __call__(self, method):
        @wraps(method)
        def _wrapper(_self, request, *args, **kwargs):
            if not self._has_perm(_self, request):
                raise exceptions.PermissionDenied()
            if not self._can_trans(request):
                raise exceptions.ValidationError('当前状态无法进行此操作')
            if not self._match_conds(_self, request):
                raise exceptions.ValidationError('该操作不具备先决条件')
            with transaction.atomic():
                ret = method(_self, request, *args, **kwargs)
                setattr(_self, self.field.attname, self.target)
                _self.save()
                return ret
        return _wrapper
