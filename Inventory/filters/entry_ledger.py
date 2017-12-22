from django_filters import rest_framework as filters

from Inventory.models import (
    WeldingMaterialEntryDetail,
    SteelMaterialEntryDetail,
    BoughtInComponentEntryDetail,
    AuxiliaryMaterialEntryDetail,
)


class AbstractEntryLedgerFilter(filters.FilterSet):
    create_dt_start = filters.DateTimeFilter(
        name='entry__create_dt', lookup_expr='gte')
    create_dt_end = filters.DateTimeFilter(
        name='entry__create_dt', lookup_expr='lte')


class WeldingMaterialEntryLedgerFilter(AbstractEntryLedgerFilter):
    material_mark = filters.CharFilter(
        name='procurement_material__process_material__name',
        lookup_expr='icontains')
    specification = filters.CharFilter(
        name='procurement_material__spec', lookup_expr='icontains')

    class Meta:
        model = WeldingMaterialEntryDetail
        fields = ('create_dt_start', 'create_dt_end', 'material_mark',
                  'specification')


class SteelMaterialEntryLedgerFilter(AbstractEntryLedgerFilter):
    work_order_uid = filters.CharFilter(
        name='entry__bidding_sheet__purchase_order__work_order__uid',
        lookup_expr='icontains')
    material_mark = filters.CharFilter(
        name='procurement_material__process_material__name',
        lookup_expr='icontains')
    specification = filters.CharFilter(
        name='procurement_material__spec', lookup_expr='icontains')

    class Meta:
        model = SteelMaterialEntryDetail
        fields = ('create_dt_start', 'create_dt_end',
                  'work_order_uid', 'material_mark', 'specification')


class BoughtInComponentEntryLedgerFilter(AbstractEntryLedgerFilter):
    work_order_uid = filters.CharFilter(
        name='entry__bidding_sheet__purchase_order__work_order__uid',
        lookup_expr='icontains')
    specification = filters.CharFilter(
        name='procurement_material__spec', lookup_expr='icontains')

    class Meta:
        model = BoughtInComponentEntryDetail
        fields = ('create_dt_start', 'create_dt_end', 'work_order_uid',
                  'specification')


class AuxiliaryMaterialEntryLedgerFilter(AbstractEntryLedgerFilter):
    specification = filters.CharFilter(
        name='procurement_material__spec', lookup_expr='icontains')
    factory = filters.CharFilter(
        name='factory', lookup_expr='icontains')
    # TODO: Replace with true field
    supplier = filters.CharFilter(
        name='factory', lookup_expr='icontains')

    class Meta:
        model = AuxiliaryMaterialEntryDetail
        fields = ('create_dt_start', 'create_dt_end', 'factory',
                  'specification', 'supplier')
