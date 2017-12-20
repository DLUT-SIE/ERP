from rest_framework import viewsets

from Inventory.models import (
    WeldingMaterialRefundCard,
    SteelMaterialRefundCard,
    BoughtInComponentRefundCard,
)
from Inventory import serializers, filters


class WeldingMaterialRefundCardViewSet(viewsets.ModelViewSet):
    queryset = WeldingMaterialRefundCard.objects.all().order_by('-pk')
    filter_class = filters.WeldingMaterialRefundCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialRefundCardListSerializer
        else:
            return serializers.WeldingMaterialRefundCardSerializer


class SteelMaterialRefundCardViewSet(viewsets.ModelViewSet):
    queryset = SteelMaterialRefundCard.objects.all().order_by('-pk')
    filter_class = filters.SteelMaterialRefundCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SteelMaterialRefundCardListSerializer
        else:
            return serializers.SteelMaterialRefundCardSerializer


class BoughtInComponentRefundCardViewSet(viewsets.ModelViewSet):
    queryset = BoughtInComponentRefundCard.objects.all().order_by('-pk')
    filter_class = filters.BoughtInComponentRefundCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BoughtInComponentRefundCardListSerializer
        else:
            return serializers.BoughtInComponentRefundCardSerializer
