from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import MaterialExecution, MaterialExecutionDetail
from Procurement import serializers
from Procurement import filters


#  材料执行表
class MaterialExecutionViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = MaterialExecution.objects.all().order_by('-pk')
    filter_class = filters.MaterialExcutionFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.MaterialExecutionCreateSerializer
        if self.action == 'list':
            return serializers.MaterialExecutionListSerializer
        else:
            return serializers.MaterialExecutionSerializer


# 材料执行表明细
class MaterialExecutionDetailViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = MaterialExecutionDetail.objects.all().filter(
        material_execution=None).order_by('-pk')
    serializer_class = serializers.MaterialExecutionDetailSerializer
