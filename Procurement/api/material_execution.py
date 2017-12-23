from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import MaterialExecution, MaterialExecutionDetail
from Procurement import serializers


class MaterialExecutionViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = MaterialExecution.objects.all().order_by('-pk')

    def perform_create(self, serializer):
        serializer.save(lister=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.MaterialExecutionCreateSerializer
        if self.action == 'list':
            return serializers.MaterialExecutionListSerializer
        else:
            return serializers.MaterialExecutionSerializer


class MaterialExecutionDetailViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = MaterialExecutionDetail.objects.all().order_by('-pk')
    serializer_class = serializers.MaterialExecutionDetailSerializer
