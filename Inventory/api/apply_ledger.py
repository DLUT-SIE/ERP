from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Inventory.models import (
    WeldingMaterialApplyCard,
    SteelMaterialApplyDetail,
    AuxiliaryMaterialApplyCard,
    BoughtInComponentApplyDetail,
)
from Inventory import serializers, filters


class WeldingMaterialApplyLedgerViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.WeldingMaterialApplyLedgerSerializer
    queryset = (WeldingMaterialApplyCard.objects.all().order_by('-pk')
                .select_related(
                    'sub_order',
                    'applicant'))
    filter_class = filters.WeldingMaterialApplyLedgerFilter


class SteelMaterialApplyLedgerViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.SteelMaterialApplyLedgerSerializer
    queryset = (SteelMaterialApplyDetail.objects.all().order_by('-pk')
                .select_related(
                    'apply_card__sub_order',
                    'process_material__material'))
    filter_class = filters.SteelMaterialApplyLedgerFilter


class AuxiliaryMaterialApplyLedgerViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.AuxiliaryMaterialApplyLedgerSerializer
    queryset = (AuxiliaryMaterialApplyCard.objects.all().order_by('-pk')
                .select_related(
                    ('apply_inventory__entry_detail__procurement_material'
                     '__process_material'),
                    ('actual_inventory__entry_detail__procurement_material'
                     '__process_material')))
    filter_class = filters.AuxiliaryMaterialApplyLedgerFilter


class BoughtInComponentApplyLedgerViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.BoughtInComponentApplyLedgerSerializer
    queryset = (BoughtInComponentApplyDetail.objects.all().order_by('-pk')
                .select_related(
                    'apply_card__sub_order',
                    'process_material__material'))
    filter_class = filters.BoughtInComponentApplyLedgerFilter
