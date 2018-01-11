from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Inventory.models import (
    WeldingMaterialEntry, SteelMaterialEntry, AuxiliaryMaterialEntry,
    BoughtInComponentEntry,)
from Inventory import serializers, filters


class WeldingMaterialEntryViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (WeldingMaterialEntry.objects.all().order_by('-pk')
                .prefetch_related('details')
                .select_related('purchaser', 'inspector', 'keeper'))
    filter_class = filters.WeldingMaterialEntryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialEntryListSerializer
        elif self.action == 'create':
            return serializers.WeldingMaterialEntryCreateSerializer
        else:
            return serializers.WeldingMaterialEntrySerializer


class SteelMaterialEntryViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (SteelMaterialEntry.objects.all().order_by('-pk')
                .prefetch_related('details')
                .select_related('purchaser', 'inspector', 'keeper'))
    filter_class = filters.SteelMaterialEntryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SteelMaterialEntryListSerializer
        elif self.action == 'create':
            return serializers.SteelMaterialEntryCreateSerializer
        else:
            return serializers.SteelMaterialEntrySerializer


class AuxiliaryMaterialEntryViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (AuxiliaryMaterialEntry.objects.all().order_by('-pk')
                .prefetch_related('details')
                .select_related('purchaser', 'inspector', 'keeper'))
    filter_class = filters.AuxiliaryMaterialEntryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AuxiliaryMaterialEntryListSerializer
        elif self.action == 'create':
            return serializers.AuxiliaryMaterialEntryCreateSerializer
        else:
            return serializers.AuxiliaryMaterialEntrySerializer


class BoughtInComponentEntryViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (BoughtInComponentEntry.objects.all().order_by('-pk')
                .prefetch_related('details')
                .select_related('purchaser', 'inspector', 'keeper'))
    filter_class = filters.BoughtInComponentEntryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BoughtInComponentEntryListSerializer
        elif self.action == 'create':
            return serializers.BoughtInComponentEntryCreateSerializer
        else:
            return serializers.BoughtInComponentEntrySerializer
