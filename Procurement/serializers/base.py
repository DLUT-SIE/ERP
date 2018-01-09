
from rest_framework import serializers
from Core.utils.serializers import DynamicFieldSerializerMixin
from Core.utils.fsm import TransitionSerializerMixin


# 实现了动态控制返回字段、状态控制的基序列化类
class BaseDynamicFieldSerializer(DynamicFieldSerializerMixin,
                                 serializers.ModelSerializer):
    pass


class BaseTransitionSerializer(TransitionSerializerMixin,
                               BaseDynamicFieldSerializer):
    pass
