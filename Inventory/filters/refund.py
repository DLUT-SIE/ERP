from django_filters import rest_framework as filters

from Inventory.models import (
    WeldingMaterialRefundCard,
    SteelMaterialRefundCard,
    BoughtInComponentRefundCard,
)


class AbstractRefundCardFilter(filters.FilterSet):
    create_dt_start = filters.DateTimeFilter(
        name='create_dt', lookup_expr='gte')
    create_dt_end = filters.DateTimeFilter(
        name='create_dt', lookup_expr='lte')
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')


class WeldingMaterialRefundCardFilter(AbstractRefundCardFilter):
    sub_order_uid = filters.CharFilter(
        name='sub_order__uid', lookup_expr='icontains')
    # TODO: Replace with right field
    welding_seam_uid = filters.CharFilter(
        name='sub_order__uid', lookup_expr='icontains')

    class Meta:
        model = WeldingMaterialRefundCard
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status',
                  'sub_order_uid', 'welding_seam_uid')


class SteelMaterialRefundCardFilter(AbstractRefundCardFilter):
    sub_order_uid = filters.CharFilter(
        name='apply_card__sub_order__uid', lookup_expr='icontains')

    class Meta:
        model = SteelMaterialRefundCard
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status',
                  'sub_order_uid')


class BoughtInComponentRefundCardFilter(AbstractRefundCardFilter):
    sub_order_uid = filters.CharFilter(
        name='apply_card__sub_order__uid', lookup_expr='icontains')
    department = filters.CharFilter(
        name='apply_card__department', lookup_expr='icontains')

    class Meta:
        model = BoughtInComponentRefundCard
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status',
                  'sub_order_uid', 'department')
