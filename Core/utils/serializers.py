from rest_framework import serializers


class DynamicFieldSerializerMixin(serializers.Serializer):
    """
    动态指定保留字段
    """
    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', None)
        super().__init__(*args, **kwargs)

        if (context and context['request']
                and 'fields' in context['request'].query_params):
            try:
                fields = context['request'].query_params['fields'].split(',')
                fields = set(fields)
            except Exception:
                fields = []
            for field in [f for f in self.fields if f not in fields]:
                self.fields.pop(field)
