from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Inventory.models import (
    WeldingMaterialEntryDetail, SteelMaterialEntryDetail,
    AuxiliaryMaterialEntryDetail, BoughtInComponentEntryDetail)
from Inventory import serializers, filters


class WeldingMaterialEntryLedgerViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.WeldingMaterialEntryLedgerSerializer
    queryset = WeldingMaterialEntryDetail.objects.all().order_by('-pk')
    filter_class = filters.WeldingMaterialEntryLedgerFilter


class SteelMaterialEntryLedgerViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.SteelMaterialEntryLedgerSerializer
    queryset = SteelMaterialEntryDetail.objects.all().order_by('-pk')
    filter_class = filters.SteelMaterialEntryLedgerFilter


class AuxiliaryMaterialEntryLedgerViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.AuxiliaryMaterialEntryLedgerSerializer
    queryset = AuxiliaryMaterialEntryDetail.objects.all().order_by('-pk')
    filter_class = filters.AuxiliaryMaterialEntryLedgerFilter


class BoughtInComponentEntryLedgerViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.BoughtInComponentEntryLedgerSerializer
    queryset = BoughtInComponentEntryDetail.objects.all().order_by('-pk')
    filter_class = filters.BoughtInComponentEntryLedgerFilter
