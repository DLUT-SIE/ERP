from django_filters import rest_framework as filters

from Process.models import (
    ProcessLibrary, ProcessMaterial, CirculationRoute, ProcessRoute,
    TransferCard, TransferCardProcess)


class ProcessLibraryFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(name='work_order__uid',
                                        lookup_expr='icontains')

    class Meta:
        model = ProcessLibrary
        fields = ('work_order_uid', )


class ProcessMaterialFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(name='lib__work_order__uid',
                                        lookup_expr='exact')

    class Meta:
        model = ProcessMaterial
        fields = ('work_order_uid', )


class CirculationRouteFilter(filters.FilterSet):
    process_material = filters.CharFilter(name='process_material__id',
                                          lookup_expr='exact')

    class Meta:
        model = CirculationRoute
        fields = ('process_material', )


class ProcessRouteFilter(filters.FilterSet):
    process_material = filters.CharFilter(name='process_material__id',
                                          lookup_expr='exact')

    class Meta:
        model = ProcessRoute
        fields = ('process_material',)


class TransferCardFilter(filters.FilterSet):
    worker_order_uid = filters.CharFilter(
        name='process_material__lib__work_order__uid',
        lookup_expr='exact')

    class Meta:
        model = TransferCard
        fields = ('worker_order_uid',)


class TransferCardProcessFilter(filters.FilterSet):
    transfer_card = filters.CharFilter(name='transfer_card__id',
                                       lookup_expr='exact')

    class Meta:
        model = TransferCardProcess
        fields = ('transfer_card',)
