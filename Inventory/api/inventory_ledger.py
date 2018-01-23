from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Inventory.models import (
    WeldingMaterialInventoryDetail, SteelMaterialInventoryDetail,
    AuxiliaryMaterialInventoryDetail, BoughtInComponentInventoryDetail)
from Inventory import serializers, filters


class WeldingMaterialInventoryLedgerViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.WeldingMaterialInventoryLedgerSerializer
    queryset = (WeldingMaterialInventoryDetail.objects.all().order_by('-pk')
                .select_related(
                    ('entry_detail__procurement_material'
                     '__process_material__material'),
                    'entry_detail__entry'))
    filter_class = filters.WeldingMaterialInventoryLedgerFilter


class SteelMaterialInventoryLedgerViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.SteelMaterialInventoryLedgerSerializer
    queryset = (SteelMaterialInventoryDetail.objects.all().order_by('-pk')
                .select_related(
                    ('entry_detail__procurement_material'
                     '__process_material__material'),
                    'entry_detail__entry',
                    'warehouse'))
    filter_class = filters.SteelMaterialInventoryLedgerFilter


class AuxiliaryMaterialInventoryLedgerViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.AuxiliaryMaterialInventoryLedgerSerializer
    queryset = (AuxiliaryMaterialInventoryDetail.objects.all().order_by('-pk')
                .select_related(
                    'entry_detail__procurement_material__process_material',
                    'entry_detail__entry'))
    filter_class = filters.AuxiliaryMaterialInventoryLedgerFilter


class BoughtInComponentInventoryLedgerViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.BoughtInComponentInventoryLedgerSerializer
    queryset = (BoughtInComponentInventoryDetail.objects.all().order_by('-pk')
                .select_related(
                    ('entry_detail__procurement_material'
                     '__process_material__material'),
                    'entry_detail__entry'))
    filter_class = filters.BoughtInComponentInventoryLedgerFilter
