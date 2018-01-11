from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Inventory.models import (
    WeldingMaterialRefundCard,
    SteelMaterialRefundCard,
    BoughtInComponentRefundCard,
)
from Inventory import serializers, filters


class WeldingMaterialRefundCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (WeldingMaterialRefundCard.objects.all().order_by('-pk')
                .select_related(
                    'apply_card',
                    'apply_card__sub_order',
                    'apply_card__process_material'))
    filter_class = filters.WeldingMaterialRefundCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialRefundCardListSerializer
        elif self.action == 'create':
            return serializers.WeldingMaterialRefundCardCreateSerializer
        else:
            return serializers.WeldingMaterialRefundCardSerializer


class SteelMaterialRefundCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (SteelMaterialRefundCard.objects.all().order_by('-pk')
                .select_related('apply_card__sub_order')
                .prefetch_related(
                    'board_details__apply_detail__process_material__material',
                    'bar_details__apply_detail__process_material__material'))
    filter_class = filters.SteelMaterialRefundCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SteelMaterialRefundCardListSerializer
        elif self.action == 'create':
            return serializers.SteelMaterialRefundCardCreateSerializer
        else:
            return serializers.SteelMaterialRefundCardSerializer


class BoughtInComponentRefundCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (BoughtInComponentRefundCard.objects.all().order_by('-pk')
                .select_related('apply_card__sub_order')
                .prefetch_related(
                    'details__apply_detail__process_material',
                    'details__apply_detail__inventory_detail__entry_detail'))
    filter_class = filters.BoughtInComponentRefundCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BoughtInComponentRefundCardListSerializer
        elif self.action == 'create':
            return serializers.BoughtInComponentRefundCardCreateSerializer
        else:
            return serializers.BoughtInComponentRefundCardSerializer
