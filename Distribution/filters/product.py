from django.db.models import Q

from django_filters import rest_framework as filters

from Distribution.models import Product


class ProductFilter(filters.FilterSet):
    """
    用于支持前端请求对产品queryset进行筛选的过滤器
    """
    department = filters.CharFilter(label='部门相关产品',
                                    method='filter_by_department')

    class Meta:
        model = Product
        fields = ('department',)

    def filter_by_department(self, queryset, name, value):
        queryset = queryset.filter(
           Q(documents__src__id=value) | Q(documents__dst__id=value))
        return queryset.distinct()
