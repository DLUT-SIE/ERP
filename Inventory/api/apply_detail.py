from rest_framework import viewsets, mixins

from Inventory.models import (
    SteelMaterialApplyDetail,
    BoughtInComponentApplyDetail,
)
from Inventory import serializers, filters


class SteelMaterialApplyDetailViewSet(mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.ListModelMixin,
                                      viewsets.GenericViewSet):
    serializer_class = serializers.SteelMaterialApplyDetailSerializer
    filter_class = filters.SteelMaterialApplyDetailFilter
    queryset = (SteelMaterialApplyDetail.objects.all().order_by('-pk')
                .select_related('process_material', 'apply_card__sub_order'))


class BoughtInComponentApplyDetailViewSet(mixins.RetrieveModelMixin,
                                          mixins.UpdateModelMixin,
                                          mixins.ListModelMixin,
                                          viewsets.GenericViewSet):
    serializer_class = serializers.BoughtInComponentApplyDetailSerializer
    filter_class = filters.BoughtInComponentApplyDetailFilter
    queryset = (BoughtInComponentApplyDetail.objects.all().order_by('-pk')
                .select_related('process_material'))
