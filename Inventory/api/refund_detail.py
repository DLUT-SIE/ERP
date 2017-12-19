from rest_framework import viewsets

from Inventory.models import (
    BoardSteelMaterialRefundDetail,
    BarSteelMaterialRefundDetail,
)
from Inventory import serializers


class BoardSteelMaterialRefundDetailViewSet(viewsets.ModelViewSet):
    queryset = BoardSteelMaterialRefundDetail.objects.all().order_by('-pk')
    serializer_class = serializers.BoardSteelMaterialRefundDetailSerializer


class BarSteelMaterialRefundDetailViewSet(viewsets.ModelViewSet):
    queryset = BarSteelMaterialRefundDetail.objects.all().order_by('-pk')
    serializer_class = serializers.BarSteelMaterialRefundDetailSerializer
