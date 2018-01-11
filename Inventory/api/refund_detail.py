from rest_framework import viewsets, mixins

from Inventory.models import (
    BoardSteelMaterialRefundDetail,
    BarSteelMaterialRefundDetail,
    BoughtInComponentRefundDetail,
)
from Inventory import serializers


class BoardSteelMaterialRefundDetailViewSet(mixins.RetrieveModelMixin,
                                            mixins.UpdateModelMixin,
                                            viewsets.GenericViewSet):
    queryset = (BoardSteelMaterialRefundDetail.objects.all().order_by('-pk')
                .select_related(
                    'apply_detail__process_material__material',
                    'refund_card__apply_card'))
    serializer_class = serializers.BoardSteelMaterialRefundDetailSerializer


class BarSteelMaterialRefundDetailViewSet(mixins.RetrieveModelMixin,
                                          mixins.UpdateModelMixin,
                                          viewsets.GenericViewSet):
    queryset = (BarSteelMaterialRefundDetail.objects.all().order_by('-pk')
                .select_related(
                    'apply_detail__process_material__material',
                    'refund_card__apply_card'))
    serializer_class = serializers.BarSteelMaterialRefundDetailSerializer


class BoughtInComponentRefundDetailViewSet(mixins.RetrieveModelMixin,
                                           mixins.UpdateModelMixin,
                                           viewsets.GenericViewSet):
    queryset = (BoughtInComponentRefundDetail.objects.all().order_by('-pk')
                .select_related(
                    'apply_detail__process_material',
                    'apply_detail__inventory_detail__entry_detail'))
    serializer_class = serializers.BoughtInComponentRefundDetailSerializer
