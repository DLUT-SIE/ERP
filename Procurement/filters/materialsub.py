from django_filters import rest_framework as filters
from Procurement import models


# 根据代用单编号模糊查询
class MaterialSubApplyFilter(filters.FilterSet):
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')

    class Meta:
        model = models.MaterialSubApply
        fields = ('uid',)
