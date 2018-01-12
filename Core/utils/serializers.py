from rest_framework import serializers, exceptions


class DynamicFieldSerializerMixin(serializers.Serializer):
    """
    动态指定保留字段
    """

    def __init__(self, *args, **kwargs):
        # 获取暴露给外部的所有字段
        fields = set()
        cls = type(self)
        for _cls in cls.mro():
            if hasattr(_cls, 'Meta') and hasattr(_cls.Meta, 'fields'):
                _fields = _cls.Meta.fields
                fields = fields | set(_fields)
        if 'default_fields' not in cls.Meta.__dict__:
            cls.Meta.default_fields = set(cls.Meta.fields)
        cls.Meta.fields = tuple(fields)
        super().__init__(*args, **kwargs)

        include_fields = self.Meta.default_fields
        context = kwargs.get('context', None)
        if (context and context['request']
                and 'fields' in context['request'].query_params):
            # 计算指定字段与所有字段的交集
            try:
                query_fields = context['request'].query_params['fields']
                query_fields = set(query_fields.split(','))
            except Exception:
                query_fields = set()
            include_fields = fields & query_fields
        for f in [f for f in self.fields if f not in include_fields]:
            self.fields.pop(f)

        # 没有字段返回, 抛出400异常
        if not self.fields:
            raise exceptions.ParseError()
