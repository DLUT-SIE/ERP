from django_filters import rest_framework as filters
from Procurement import models


# 根据代用单编号模糊查询
class MaterialExcutionFilter(filters.FilterSet):
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')

    class Meta:
        model = models.MaterialExecution
        fields = ('uid',)


# 根据材料执行表模糊查询
class MaterialExecutionDetailFilter(filters.FilterSet):
    class Meta:
        model = models.MaterialExecutionDetail
        fields = ('material_execution',)
