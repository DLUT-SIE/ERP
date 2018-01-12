from django_filters import rest_framework as filters

from Inventory.models import (
    SteelMaterialApplyDetail,
    BoughtInComponentApplyDetail,
)


class SteelMaterialApplyDetailFilter(filters.FilterSet):
    apply_card_uid = filters.CharFilter(name='apply_card__uid',
                                        lookup_expr='exact')

    class Meta:
        model = SteelMaterialApplyDetail
        fields = ('apply_card_uid',)


class BoughtInComponentApplyDetailFilter(filters.FilterSet):
    apply_card_uid = filters.CharFilter(name='apply_card__uid',
                                        lookup_expr='exact')

    class Meta:
        model = BoughtInComponentApplyDetail
        fields = ('apply_card_uid',)
