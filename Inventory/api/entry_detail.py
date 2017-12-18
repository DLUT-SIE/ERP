from rest_framework import viewsets

from Inventory.models import (
    WeldingMaterialEntryDetail, SteelMaterialEntryDetail,
    AuxiliaryMaterialEntryDetail, BoughtInComponentEntryDetail)
from Inventory import serializers


class WeldingMaterialEntryDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WeldingMaterialEntryDetailSerializer
    queryset = WeldingMaterialEntryDetail.objects.all().order_by('-pk')


class SteelMaterialEntryDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SteelMaterialEntryDetailSerializer
    queryset = SteelMaterialEntryDetail.objects.all().order_by('-pk')


class AuxiliaryMaterialEntryDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuxiliaryMaterialEntryDetailSerializer
    queryset = AuxiliaryMaterialEntryDetail.objects.all().order_by('-pk')


class BoughtInComponentEntryDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BoughtInComponentEntryDetailSerializer
    queryset = BoughtInComponentEntryDetail.objects.all().order_by('-pk')
