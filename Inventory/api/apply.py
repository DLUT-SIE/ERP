from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Inventory.models import (
    WeldingMaterialApplyCard,
    SteelMaterialApplyCard,
    AuxiliaryMaterialApplyCard,
    BoughtInComponentApplyCard,
)
from Inventory import serializers, filters


class WeldingMaterialApplyCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingMaterialApplyCard.objects.all().order_by('-pk')
    filter_class = filters.WeldingMaterialApplyCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialApplyCardListSerializer
        else:
            return serializers.WeldingMaterialApplyCardSerializer


class SteelMaterialApplyCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SteelMaterialApplyCard.objects.all().order_by('-pk')
    filter_class = filters.SteelMaterialApplyCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SteelMaterialApplyCardListSerializer
        else:
            return serializers.SteelMaterialApplyCardSerializer


class AuxiliaryMaterialApplyCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = AuxiliaryMaterialApplyCard.objects.all().order_by('-pk')
    filter_class = filters.AuxiliaryMaterialApplyCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AuxiliaryMaterialApplyCardListSerializer
        else:
            return serializers.AuxiliaryMaterialApplyCardSerializer


class BoughtInComponentApplyCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = BoughtInComponentApplyCard.objects.all().order_by('-pk')
    filter_class = filters.BoughtInComponentApplyCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BoughtInComponentApplyCardListSerializer
        else:
            return serializers.BoughtInComponentApplyCardSerializer
