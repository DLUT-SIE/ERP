from rest_framework import viewsets

from Inventory.models import (
    WeldingMaterialApplyCard,
    SteelMaterialApplyCard,
    AuxiliaryMaterialApplyCard,
    BoughtInComponentApplyCard,
)
from Inventory import serializers


class WeldingMaterialApplyCardViewSet(viewsets.ModelViewSet):
    queryset = WeldingMaterialApplyCard.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialApplyCardListSerializer
        else:
            return serializers.WeldingMaterialApplyCardSerializer


class SteelMaterialApplyCardViewSet(viewsets.ModelViewSet):
    queryset = SteelMaterialApplyCard.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SteelMaterialApplyCardListSerializer
        else:
            return serializers.SteelMaterialApplyCardSerializer


class AuxiliaryMaterialApplyCardViewSet(viewsets.ModelViewSet):
    queryset = AuxiliaryMaterialApplyCard.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AuxiliaryMaterialApplyCardListSerializer
        else:
            return serializers.AuxiliaryMaterialApplyCardSerializer


class BoughtInComponentApplyCardViewSet(viewsets.ModelViewSet):
    queryset = BoughtInComponentApplyCard.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BoughtInComponentApplyCardListSerializer
        else:
            return serializers.BoughtInComponentApplyCardSerializer
