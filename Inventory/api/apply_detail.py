from rest_framework import viewsets

from Inventory.models import (
    SteelMaterialApplyDetail,
    BoughtInComponentApplyDetail,
)
from Inventory import serializers


class SteelMaterialApplyDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SteelMaterialApplyDetailSerializer
    queryset = SteelMaterialApplyDetail.objects.all().order_by('-pk')


class BoughtInComponentApplyDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BoughtInComponentApplyDetailSerializer
    queryset = BoughtInComponentApplyDetail.objects.all().order_by('-pk')
