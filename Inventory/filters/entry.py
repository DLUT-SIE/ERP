from django_filters import rest_framework as filters

from Inventory.models import (
    WeldingMaterialEntry,
    SteelMaterialEntry,
    BoughtInComponentEntry,
    AuxiliaryMaterialEntry,
)


class AbstractEntryFilter(filters.FilterSet):
    create_dt_start = filters.DateTimeFilter(
        name='create_dt', lookup_expr='gte')
    create_dt_end = filters.DateTimeFilter(
        name='create_dt', lookup_expr='lte')
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')


class WeldingMaterialEntryFilter(AbstractEntryFilter):
    class Meta:
        model = WeldingMaterialEntry
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status')


class SteelMaterialEntryFilter(AbstractEntryFilter):
    source = filters.CharFilter(name='source', lookup_expr='icontains')

    class Meta:
        model = SteelMaterialEntry
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status',
                  'source')


class BoughtInComponentEntryFilter(AbstractEntryFilter):
    source = filters.CharFilter(name='source', lookup_expr='icontains')

    class Meta:
        model = BoughtInComponentEntry
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status',
                  'source', 'category')


class AuxiliaryMaterialEntryFilter(AbstractEntryFilter):
    class Meta:
        model = AuxiliaryMaterialEntry
        fields = ('create_dt_start', 'create_dt_end', 'uid', 'status')
