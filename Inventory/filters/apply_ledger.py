from django_filters import rest_framework as filters

from Inventory.models import (
    WeldingMaterialApplyCard,
    SteelMaterialApplyDetail,
    BoughtInComponentApplyDetail,
    AuxiliaryMaterialApplyCard,
)


class AbstractApplyLedgerFilter(filters.FilterSet):
    create_dt_start = filters.DateTimeFilter(
        name='create_dt', lookup_expr='gte')
    create_dt_end = filters.DateTimeFilter(
        name='create_dt', lookup_expr='lte')


class AbstractApplyDetailLedgerFilter(filters.FilterSet):
    create_dt_start = filters.DateTimeFilter(
        name='apply_card__create_dt', lookup_expr='gte')
    create_dt_end = filters.DateTimeFilter(
        name='apply_card__create_dt', lookup_expr='lte')


class WeldingMaterialApplyLedgerFilter(AbstractApplyLedgerFilter):
    sub_order_uid = filters.CharFilter(name='sub_order',
                                       method='filter_sub_order_uid')
    # TODO: Replace with true field
    welding_seam_uid = filters.CharFilter(name='uid', lookup_expr='icontains')
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')

    class Meta:
        model = WeldingMaterialApplyCard
        fields = ('create_dt_start', 'create_dt_end', 'sub_order_uid',
                  'welding_seam_uid', 'uid')

    def filter_sub_order_uid(self, queryset, name, value):
        splits = value.rsplit('-', 1)  # eg, WO1234-1
        if len(splits) == 1:  # Only WorkOrder provided, fuzzy match
            work_order_uid = splits[0]
            return queryset.filter(
                sub_order__work_order__uid__icontains=work_order_uid)
        else:
            work_order_uid, index = splits
            index = int(index)
            return queryset.filter(sub_order__work_order_uid=work_order_uid,
                                   sub_order__index=index)


class SteelMaterialApplyLedgerFilter(AbstractApplyDetailLedgerFilter):
    specification = filters.CharFilter(
        name='procuremnt_material__process_material__spec',
        lookup_expr='icontains')
    material_number = filters.CharFilter(
        name='procurement_material__process_material__material__uid',
        lookup_expr='icontains')
    material_mark = filters.CharFilter(
        name='procurement_material__process_material__name',
        lookup_expr='icontains')

    class Meta:
        model = SteelMaterialApplyDetail
        fields = ('create_dt_start', 'create_dt_end', 'specification',
                  'material_number', 'material_mark')


class BoughtInComponentApplyLedgerFilter(AbstractApplyDetailLedgerFilter):
    specification = filters.CharFilter(
        name='procuremnt_material__process_material__spec',
        lookup_expr='icontains')
    sub_order_uid = filters.CharFilter(name='sub_order',
                                       method='filter_sub_order_uid')

    class Meta:
        model = BoughtInComponentApplyDetail
        fields = ('create_dt_start', 'create_dt_end', 'sub_order_uid',
                  'specification')

    def filter_sub_order_uid(self, queryset, name, value):
        splits = value.rsplit('-', 1)  # eg, WO1234-1
        if not splits:
            return queryset
        elif len(splits) > 1:
            uid, index = splits
            index = int(index)
            return queryset.filter(
                apply_card__sub_order__work_order__uid=uid,
                apply_card__sub_order__index=index)
        else:
            uid = splits[0]
            return queryset.filter(
                apply_card__sub_order__work_order__uid__icontains=uid)


class AuxiliaryMaterialApplyLedgerFilter(AbstractApplyLedgerFilter):
    department = filters.CharFilter(
        name='department', lookup_expr='icontains')
    apply_card_uid = filters.CharFilter(
        name='uid', lookup_expr='icontains')

    class Meta:
        model = AuxiliaryMaterialApplyCard
        fields = ('create_dt_start', 'create_dt_end',
                  'department', 'apply_card_uid')
