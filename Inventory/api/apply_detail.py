from rest_framework import viewsets, mixins

from Inventory.models import (
    SteelMaterialApplyDetail,
    BoughtInComponentApplyDetail,
)
from Inventory import serializers


class SteelMaterialApplyDetailViewSet(mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.ListModelMixin,
                                      viewsets.GenericViewSet):
    serializer_class = serializers.SteelMaterialApplyDetailSerializer
    queryset = SteelMaterialApplyDetail.objects.all().order_by('-pk')


class BoughtInComponentApplyDetailViewSet(mixins.RetrieveModelMixin,
                                          mixins.UpdateModelMixin,
                                          mixins.ListModelMixin,
                                          viewsets.GenericViewSet):
    serializer_class = serializers.BoughtInComponentApplyDetailSerializer
    queryset = BoughtInComponentApplyDetail.objects.all().order_by('-pk')
