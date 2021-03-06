from functools import partial
from collections import Iterable, defaultdict

from django.db import transaction
from django.db.models.base import ModelBase
from django.core import exceptions

from rest_framework import serializers


class Transition:
    def __init__(self, method, field, source, target,
                 conditions=None, permission=None, name=None):
        self.method = method
        self.field_name = field
        self.source = source
        self.target = target
        self.conditions = conditions
        self.permission = permission
        self._field_name = name
        self.inst = None

    @property
    def name(self):
        if self._field_name is not None:
            return self._field_name
        return self.method.__name__

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

    def _match_source(self, inst, request):
        """
        检查前置状态
        """
        current_status = getattr(inst, self.field_name)
        if self.source == current_status or self.source == '*':
            return True
        elif (not isinstance(self.source, str) and
                isinstance(self.source, Iterable)):
            return current_status in self.source
        else:
            return False

    def _match_conds(self, inst, request):
        """
        检查附件条件
        """
        if self.conditions is None:
            valid_conds_func = getattr(
                inst, 'valid_{}'.format(self.method.__name__), lambda x: True)
            return valid_conds_func(request)
        elif isinstance(self.conditions, str):
            valid_conds_func = getattr(inst, self.conditions, lambda x: True)
            return valid_conds_func(request)
        elif isinstance(self.conditions, bool):
            return self.conditions
        elif callable(self.conditions):
            return self.conditions(inst, request)
        else:
            return False

    def check_validity(self, inst, request, raise_exception=True):
        if not self._has_perm(inst, request):
            if raise_exception:
                raise exceptions.PermissionDenied()
            else:
                return False
        if not self._match_source(inst, request):
            if raise_exception:
                raise exceptions.ValidationError('当前状态无法进行此操作')
            else:
                return False
        if not self._match_conds(inst, request):
            if raise_exception:
                raise exceptions.ValidationError('该操作不满足附加条件')
            else:
                return False
        return True

    def __get__(self, instance, owner):
        self.inst = instance
        return self

    def __call__(self, request, *args, **kwargs):
        inst = self.inst
        self.check_validity(inst, request)
        ret = self.method(inst, request, *args, **kwargs)
        setattr(inst, self.field_name, self.target)
        return ret


def transition(field, source, target, conditions=None,
               permission=None, name=None):
    """
    用于控制工作流状态转移的方法装饰器

    Parameters
    ------------
    field
        进行状态转移的字段名称
    source
        起始状态, 使用'*'表示任意状态
    target
        目标状态, 完成对应操作后转入状态
    conditions(可选)
        进行该状态转移所需的额外条件, 若未设置, 则默认会查找
    `valid_+<转移函数名>`的方法进行检查, 若不存在跳过该检查, 若为`str`类型,则\
    在调用实例上查找同名函数并返回其调用结果, 若为'bool'类型, 则在检查时直接返\
    回该值, 若为函数, 则在检查时接收实例变量`inst`以及'request'作为参数并返回\
    其调用结果, 否则不允许操作
    permission(可选)
        进行该状态转移所需的权限, 默认跳过该检查, 若为'bool'类型，则在检查时直\
    接返回该值, 若为'str'类型, 则根据'user.has_perm'进行判断, 若为函数, 则在检\
    查时接收一个参数'request'并返回其调用结果, 否则不允许操作
    name(可选)
        设置该字段在向前台进行渲染时的名称, 默认为方法名

    Example
    ---------
    .. code:: python

        from Core.utils import transition


        class Example(models.Model):
            status = models.IntegerField(verbose_name='状态',
                                         choices=REVIEW_STATUS_CHOICES,
                                         default=REVIEW_STATUS_DEFAULT)

            @transition(field='status', source='*', target=REVIEW_STATUS_PASS)
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


    :作者:
        杜佑宸 <youchen.du@gmail.com>

    """
    def _wraps(method):
        return Transition(method, field, source, target,
                          conditions, permission, name)
    return _wraps


def valid_actions(inst, request=None):
    actions = defaultdict(partial(defaultdict, int))
    for name, trans in inst.transitions.items():
        if trans.check_validity(inst, request, raise_exception=False):
            actions[trans.field_name][trans.name] = trans.target
    return actions


class TransitionMeta(ModelBase):
    """
    用于向Model对象添加自动生成当前状态下可选操作方法的元类

    该元类将自动向实例添加一个实例方法 `actions`, 该方法接收一个参数 `request`,
    返回当前实例下所有使用 `transition` 装饰的当前可用操作目标结果,该元类主要
    为向前台提供当前可用操作提供服务。

    Example
    ---------
    .. code:: python

        from Core.utils.fsm import TransitionMeta


        class Example(models.Model, metaclass=TransitionMeta):
            status = models.IntegerField(verbose_name='状态',
                                         choices=REVIEW_STATUS_CHOICES,
                                         default=REVIEW_STATUS_DEFAULT)

            @transition(field='status', source='*', target=REVIEW_STATUS_PASS)
            def review_pass(self, request):
                # Do some relavent actions
                # status will be updated and saved automatically
                pass
    """
    def __new__(cls, name, bases, attrs, **kwargs):
        transitions = {}
        for base in bases:
            if hasattr(base, 'transitions'):
                transitions.update(getattr(base, 'transitions'))
        for attr_name, attr in attrs.items():
            # TODO: Check incompatible Transition(eg. same source and target)
            # Raise Exception
            if isinstance(attr, Transition):
                transitions[attr_name] = attr
        attrs['transitions'] = transitions
        attrs['actions'] = valid_actions
        return super().__new__(cls, name, bases, attrs, **kwargs)


class TransitionSerializerMixin(serializers.Serializer):
    """
    用于向Serializer对象添加额外字段 `actions` 的Mixin组件,配合其他相关组件使用

    Example
    --------
    .. code:: python

        from Core.utils.fsm import TransitionSerializerMixin as TSMixin


        class ProductSerializer(TSMixin, serializers.ModelSerializer):
            documents = serializers.PrimaryKeyRelatedField(many=True,
                                                           read_only=True)

            class Meta:
                model = Product
                fields = '__all__'
                read_only_fields = ('name',)
    """
    actions = serializers.SerializerMethodField()

    def get_actions(self, obj):
        actions = obj.actions(self.context['request'])
        return actions

    def _run_transitions_validator(self, attrs):
        inst = self.instance
        request = self.context['request']
        trans_map = defaultdict(list)
        for name, trans in inst.transitions.items():
            trans_map[trans.field_name].append(trans)
        errors = {}
        self.__attr_trans = {}
        for attr in (attr for attr in attrs if attr in trans_map and
                     not getattr(inst, attr) == attrs[attr]):
            valid_trans = [trans for trans in trans_map[attr]
                           if trans._match_source(inst, request) and
                           trans.target == attrs[attr]]
            if not valid_trans:
                errors[attr] = '该操作无效'
                continue
            trans = valid_trans[0]
            self.__attr_trans[attr] = trans.method.__name__
            try:
                trans.check_validity(inst, request, raise_exception=True)
            except (serializers.ValidationError,
                    exceptions.ValidationError) as err:
                errors[attr] = err.message
        if errors:
            raise serializers.ValidationError(errors)

    def run_validators(self, attrs):
        super().run_validators(attrs)
        if self.instance:  # Only validate on update
            self._run_transitions_validator(attrs)
        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            for attr, trans_name in self.__attr_trans.items():
                validated_data.pop(attr)
                getattr(instance, trans_name)(self.context['request'])
            return super().update(instance, validated_data)
