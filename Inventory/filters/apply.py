from django_filters import rest_framework as filters

from Inventory.models import (
    WeldingMaterialApplyCard,
    SteelMaterialApplyCard,
    BoughtInComponentApplyCard,
    AuxiliaryMaterialApplyCard,
)


class AbstractApplyCardFilter(filters.FilterSet):
    create_dt_start = filters.DateTimeFilter(
        name='create_dt', lookup_expr='gte')
    create_dt_end = filters.DateTimeFilter(
        name='create_dt', lookup_expr='lte')
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')


class WeldingMaterialApplyCardFilter(AbstractApplyCardFilter):
    sub_order_uid = filters.CharFilter(
        name='sub_order__uid', lookup_expr='icontains')
    material_mark = filters.CharFilter(
        name='procurement_material__process_material__name',
        lookup_expr='icontains')
    # TODO: Replace with right field
    model = filters.CharFilter(
        name='uid', lookup_expr='icontains')

    class Meta:
        model = WeldingMaterialApplyCard
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status',
                  'sub_order_uid', 'material_mark', 'model')


class SteelMaterialApplyCardFilter(AbstractApplyCardFilter):
    class Meta:
        model = SteelMaterialApplyCard
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status')


class BoughtInComponentApplyCardFilter(AbstractApplyCardFilter):
    sub_order_uid = filters.CharFilter(
        name='sub_order__uid', lookup_expr='icontains')
    department = filters.CharFilter(
        name='department', lookup_expr='icontains')

    class Meta:
        model = BoughtInComponentApplyCard
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status',
                  'sub_order_uid', 'department')


class AuxiliaryMaterialApplyCardFilter(AbstractApplyCardFilter):
    department = filters.CharFilter(
        name='department', lookup_expr='icontains')

    class Meta:
        model = AuxiliaryMaterialApplyCard
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status',
                  'apply_inventory', 'department')
