from rest_framework import viewsets, mixins

from Inventory.models import (
    BoardSteelMaterialRefundDetail,
    BarSteelMaterialRefundDetail,
)
from Inventory import serializers


class BoardSteelMaterialRefundDetailViewSet(mixins.RetrieveModelMixin,
                                            mixins.UpdateModelMixin,
                                            mixins.ListModelMixin,
                                            viewsets.GenericViewSet):
    queryset = BoardSteelMaterialRefundDetail.objects.all().order_by('-pk')
    serializer_class = serializers.BoardSteelMaterialRefundDetailSerializer


class BarSteelMaterialRefundDetailViewSet(mixins.RetrieveModelMixin,
                                          mixins.UpdateModelMixin,
                                          mixins.ListModelMixin,
                                          viewsets.GenericViewSet):
    queryset = BarSteelMaterialRefundDetail.objects.all().order_by('-pk')
    serializer_class = serializers.BarSteelMaterialRefundDetailSerializer
