from rest_framework import viewsets

from Inventory.models import (
    WeldingMaterialInventoryDetail, SteelMaterialInventoryDetail,
    AuxiliaryMaterialInventoryDetail, BoughtInComponentInventoryDetail)
from Inventory import serializers


class WeldingMaterialInventoryDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WeldingMaterialInventoryDetailSerializer
    queryset = (WeldingMaterialInventoryDetail.objects.all().order_by('-pk')
                .select_related('entry_detail'))


class SteelMaterialInventoryDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SteelMaterialInventoryDetailSerializer
    queryset = (SteelMaterialInventoryDetail.objects.all().order_by('-pk')
                .select_related('entry_detail'))


class AuxiliaryMaterialInventoryDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuxiliaryMaterialInventoryDetailSerializer
    queryset = (AuxiliaryMaterialInventoryDetail.objects.all().order_by('-pk')
                .select_related('entry_detail'))


class BoughtInComponentInventoryDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BoughtInComponentInventoryDetailSerializer
    queryset = (BoughtInComponentInventoryDetail.objects.all().order_by('-pk')
                .select_related('entry_detail'))
