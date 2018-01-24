from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Inventory.models import (
    Warehouse,
    WeldingMaterialHumitureRecord,
    WeldingMaterialBakeRecord,
)

from Inventory import serializers, filters


class WarehouseViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = Warehouse.objects.all().order_by('-pk')
    serializer_class = serializers.WarehouseSerializer
    filter_class = filters.WarehouseFilter


class WeldingMaterialHumitureRecordViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingMaterialHumitureRecord.objects.all().order_by('-pk')
    filter_class = filters.WeldingMaterialHumitureRecordFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialHumitureRecordListSerializer
        else:
            return serializers.WeldingMaterialHumitureRecordSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(keeper=user)


class WeldingMaterialBakeRecordViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingMaterialBakeRecord.objects.all().order_by('-pk')
    filter_class = filters.WeldingMaterialBakeRecordFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialBakeRecordListSerializer
        else:
            return serializers.WeldingMaterialBakeRecordSerializer
