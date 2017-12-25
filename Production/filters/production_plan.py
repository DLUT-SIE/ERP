from django_filters import rest_framework as filters

from Production.models import ProductionPlan


class ProductionPlanFilter(filters.FilterSet):
    """
    用于支持前端请求对生产计划queryset进行筛选的过滤器
    """
    plan_start_time = filters.DateTimeFilter(
        label='计划年月开始', name='plan_dt', lookup_expr='gte')
    plan_end_time = filters.DateTimeFilter(
        label='计划年月终止', name='plan_dt', lookup_expr='lte')
    work_order_uid = filters.CharFilter(label='工作令', name='work_order__uid',
                                        lookup_expr='icontains')

    class Meta:
        model = ProductionPlan
        fields = ('work_order_uid', 'status',
                  'plan_start_time', 'plan_end_time')
