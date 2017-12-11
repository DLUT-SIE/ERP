from django.db.models import Q

from django_filters import rest_framework as filters

from Distribution.models import Product


class ProductFilter(filters.FilterSet):
    """
    用于支持前端请求对产品queryset进行筛选的过滤器
    """
    related = filters.CharFilter(label='相关产品', method='related_filter')

    class Meta:
        model = Product
        fields = ('related',)

    def related_filter(self, queryset, name, value):
        queryset = queryset.filter(
           Q(documents__src__id=value) | Q(documents__dst__id=value))
        return queryset.distinct()
