from django_filters import rest_framework as filters

from Process.models import ProcessLibrary, ProcessMaterial


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
