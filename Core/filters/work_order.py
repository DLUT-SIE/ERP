from django_filters import rest_framework as filters

from Core.models import SubWorkOrder


class SubWorkOrderFilter(filters.FilterSet):
    """
    用于支持前端请求对子工作令queryset进行筛选的过滤器
    """
    work_order_uid = filters.CharFilter(name='work_order__uid',
                                        lookup_expr='icontains')
    index = filters.NumberFilter(name='index')
    finished = filters.BooleanFilter(name='finished')

    class Meta:
        model = SubWorkOrder
        fields = ('work_order_uid', 'index', 'finished')
