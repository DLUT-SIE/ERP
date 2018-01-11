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
    queryset = (WeldingMaterialApplyCard.objects.all().order_by('-pk')
                .select_related('sub_order', 'process_material'))
    filter_class = filters.WeldingMaterialApplyCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialApplyCardListSerializer
        elif self.action == 'create':
            return serializers.WeldingMaterialApplyCardCreateSerializer
        else:
            return serializers.WeldingMaterialApplyCardSerializer


class SteelMaterialApplyCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (SteelMaterialApplyCard.objects.all().order_by('-pk')
                .prefetch_related('details', 'details__process_material'))
    filter_class = filters.SteelMaterialApplyCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SteelMaterialApplyCardListSerializer
        elif self.action == 'create':
            return serializers.SteelMaterialApplyCardCreateSerializer
        else:
            return serializers.SteelMaterialApplyCardSerializer


class AuxiliaryMaterialApplyCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (AuxiliaryMaterialApplyCard.objects.all().order_by('-pk')
                .select_related(
                    'apply_inventory__entry_detail__procurement_material',
                    'actual_inventory__entry_detail__procurement_material',
                    'sub_order'))
    filter_class = filters.AuxiliaryMaterialApplyCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AuxiliaryMaterialApplyCardListSerializer
        elif self.action == 'create':
            return serializers.AuxiliaryMaterialApplyCardCreateSerializer
        else:
            return serializers.AuxiliaryMaterialApplyCardSerializer


class BoughtInComponentApplyCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (BoughtInComponentApplyCard.objects.all().order_by('-pk')
                .prefetch_related('details__process_material')
                .select_related('sub_order'))
    filter_class = filters.BoughtInComponentApplyCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BoughtInComponentApplyCardListSerializer
        elif self.action == 'create':
            return serializers.BoughtInComponentApplyCardCreateSerializer
        else:
            return serializers.BoughtInComponentApplyCardSerializer
