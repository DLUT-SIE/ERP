from rest_framework import viewsets

from Inventory.models import (
    Warehouse,
    WeldingMaterialHumitureRecord,
    WeldingMaterialBakeRecord,
)

from Inventory import serializers


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all().order_by('-pk')
    serializer_class = serializers.WarehouseSerializer


class WeldingMaterialHumitureRecordViewSet(viewsets.ModelViewSet):
    queryset = WeldingMaterialHumitureRecord.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialHumitureRecordListSerializer
        else:
            return serializers.WeldingMaterialHumitureRecordSerializer


class WeldingMaterialBakeRecordViewSet(viewsets.ModelViewSet):
    queryset = WeldingMaterialBakeRecord.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialBakeRecordListSerializer
        else:
            return serializers.WeldingMaterialBakeRecordSerializer
