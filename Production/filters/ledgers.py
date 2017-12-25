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

    class Meta:
        model = SubMaterial
        fields = ('sub_order', 'ticket_number', 'parent_drawing_number')
