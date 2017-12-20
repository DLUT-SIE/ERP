from django_filters import rest_framework as filters

from Inventory.models import (
    Warehouse,
    WeldingMaterialHumitureRecord,
    WeldingMaterialBakeRecord,
)


class WarehouseFilter(filters.FilterSet):
    name = filters.CharFilter(name='name', lookup_expr='icontains')
    location = filters.CharFilter(name='location', lookup_expr='icontains')

    class Meta:
        model = Warehouse
        fields = ('name', 'location', 'category')


class WeldingMaterialHumitureRecordFilter(filters.FilterSet):
    create_dt_start = filters.DateTimeFilter(
        name='create_dt', lookup_expr='gte')
    create_dt_end = filters.DateTimeFilter(
        name='create_dt', lookup_expr='lte')

    class Meta:
        model = WeldingMaterialHumitureRecord
        fields = ('create_dt_start', 'create_dt_end')


class WeldingMaterialBakeRecordFilter(filters.FilterSet):
    create_dt_start = filters.DateTimeFilter(
        name='create_dt', lookup_expr='gte')
    create_dt_end = filters.DateTimeFilter(
        name='create_dt', lookup_expr='lte')

    class Meta:
        model = WeldingMaterialBakeRecord
        fields = ('create_dt_start', 'create_dt_end', 'standard_num')
