from rest_framework import viewsets

from Inventory.models import (
    WeldingMaterialEntry, SteelMaterialEntry, AuxiliaryMaterialEntry,
    BoughtInComponentEntry,)
from Inventory import serializers, filters


class WeldingMaterialEntryViewSet(viewsets.ModelViewSet):
    queryset = WeldingMaterialEntry.objects.all().order_by('-pk')
    filter_class = filters.WeldingMaterialEntryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialEntryListSerializer
        else:
            return serializers.WeldingMaterialEntrySerializer


class SteelMaterialEntryViewSet(viewsets.ModelViewSet):
    queryset = SteelMaterialEntry.objects.all().order_by('-pk')
    filter_class = filters.SteelMaterialEntryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SteelMaterialEntryListSerializer
        else:
            return serializers.SteelMaterialEntrySerializer


class AuxiliaryMaterialEntryViewSet(viewsets.ModelViewSet):
    queryset = AuxiliaryMaterialEntry.objects.all().order_by('-pk')
    filter_class = filters.AuxiliaryMaterialEntryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AuxiliaryMaterialEntryListSerializer
        else:
            return serializers.AuxiliaryMaterialEntrySerializer


class BoughtInComponentEntryViewSet(viewsets.ModelViewSet):
    queryset = BoughtInComponentEntry.objects.all().order_by('-pk')
    filter_class = filters.BoughtInComponentEntryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BoughtInComponentEntryListSerializer
        else:
            return serializers.BoughtInComponentEntrySerializer
