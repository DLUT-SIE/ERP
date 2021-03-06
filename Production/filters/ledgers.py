from django_filters import rest_framework as filters

from Production.models import SubMaterial


class SubMaterialLedgersFilter(filters.FilterSet):
    """
    用于支持前端请求对子工作票台账queryset进行筛选的过滤器
    """
    ticket_number = filters.CharFilter(name='material__ticket_number',
                                       label='工作票号')
    parent_drawing_number = filters.CharFilter(
        name='material__parent_drawing_number', label='部件图号')
    sub_order_uid = filters.CharFilter(label='工作令', name='sub_order',
                                       method='filter_sub_order_uid')

    class Meta:
        model = SubMaterial
        fields = ('sub_order_uid', 'ticket_number', 'parent_drawing_number')

    def filter_sub_order_uid(self, queryset, name, value):
        splits = value.rsplit('-', 1)  # eg, WO1234-1
        if not splits:
            return queryset
        elif len(splits) > 1:
            uid, index = splits
            index = int(index)
            return queryset.filter(
                sub_order__work_order__uid=uid,
                sub_order__index=index)
        else:
            uid = splits[0]
            return queryset.filter(
                sub_order__work_order__uid__icontains=uid)
