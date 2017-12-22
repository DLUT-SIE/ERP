from django_filters import rest_framework as filters

from Inventory.models import (
    WeldingMaterialInventoryDetail,
    SteelMaterialInventoryDetail,
    BoughtInComponentInventoryDetail,
    AuxiliaryMaterialInventoryDetail,
)


class AbstractInventoryLedgerFilter(filters.FilterSet):
    create_dt_start = filters.DateTimeFilter(
        name='entry_detail__entry__create_dt', lookup_expr='gte')
    create_dt_end = filters.DateTimeFilter(
        name='entry_detail__entry__create_dt', lookup_expr='lte')


class WeldingMaterialInventoryLedgerFilter(AbstractInventoryLedgerFilter):
    material_mark = filters.CharFilter(
        name='entry_detail__procurement_material__process_material__name',
        lookup_expr='icontains')
    specification = filters.CharFilter(
        name='entry_detail__procurement_material__spec',
        lookup_expr='icontains')

    class Meta:
        model = WeldingMaterialInventoryDetail
        fields = ('create_dt_start', 'create_dt_end', 'material_mark',
                  'specification')


class SteelMaterialInventoryLedgerFilter(AbstractInventoryLedgerFilter):
    work_order_uid = filters.CharFilter(
        name=('entry_detail__entry__bidding_sheet'
              '__purchase_order__work_order__uid'),
        lookup_expr='icontains')
    material_mark = filters.CharFilter(
        name='entry_detail__procurement_material__process_material__name',
        lookup_expr='icontains')
    specification = filters.CharFilter(
        name='entry_detail__procurement_material__spec',
        lookup_expr='icontains')

    class Meta:
        model = SteelMaterialInventoryDetail
        fields = ('create_dt_start', 'create_dt_end',
                  'work_order_uid', 'material_mark', 'specification')


class BoughtInComponentInventoryLedgerFilter(AbstractInventoryLedgerFilter):
    work_order_uid = filters.CharFilter(
        name=('entry_detail__entry__bidding_sheet'
              '__purchase_order__work_order__uid'),
        lookup_expr='icontains')
    specification = filters.CharFilter(
        name='entry_detail__procurement_material__spec',
        lookup_expr='icontains')

    class Meta:
        model = BoughtInComponentInventoryDetail
        fields = ('create_dt_start', 'create_dt_end', 'work_order_uid',
                  'specification')


class AuxiliaryMaterialInventoryLedgerFilter(AbstractInventoryLedgerFilter):
    specification = filters.CharFilter(
        name='entry_detail__procurement_material__spec',
        lookup_expr='icontains')
    factory = filters.CharFilter(
        name='entry_detail__factory', lookup_expr='icontains')
    # TODO: Replace with true field
    supplier = filters.CharFilter(
        name='entry_detail__factory', lookup_expr='icontains')

    class Meta:
        model = AuxiliaryMaterialInventoryDetail
        fields = ('create_dt_start', 'create_dt_end', 'factory',
                  'specification', 'supplier')
