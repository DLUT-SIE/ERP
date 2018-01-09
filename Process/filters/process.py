from django_filters import rest_framework as filters

from Core.models import WorkOrder
from Process import MATERIAL_CATEGORY_CHOICES
from Process.models import (
    ProcessLibrary, ProcessMaterial, CirculationRoute, ProcessRoute, Material,
    TransferCard, TransferCardProcess, BoughtInItem, FirstFeedingItem,
    CooperantItem, PrincipalQuotaItem, QuotaList, WeldingQuotaItem,
    AuxiliaryQuotaItem, WeldingSeam, TotalWeldingMaterial, WeldingMaterial,
    FluxMaterial, WeldingProcessSpecification, WeldingJointProcessAnalysis,
    WeldingCertification, WeldingWorkInstruction)


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
    work_order_uid = filters.CharFilter(
        name='process_material__lib__work_order__uid',
        lookup_expr='exact')

    class Meta:
        model = TransferCard
        fields = ('work_order_uid',)


class TransferCardProcessFilter(filters.FilterSet):
    transfer_card = filters.CharFilter(name='transfer_card__id',
                                       lookup_expr='exact')

    class Meta:
        model = TransferCardProcess
        fields = ('transfer_card',)


class BoughtInItemFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(
        name='process_material__lib__work_order__uid',
        lookup_expr='exact')

    class Meta:
        model = BoughtInItem
        fields = ('work_order_uid',)


class FirstFeedingItemFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(
        name='process_material__lib__work_order__uid',
        lookup_expr='exact')

    class Meta:
        model = FirstFeedingItem
        fields = ('work_order_uid',)


class CooperantItemFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(
        name='process_material__lib__work_order__uid',
        lookup_expr='exact')

    class Meta:
        model = CooperantItem
        fields = ('work_order_uid',)


class AbstractQuotaFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(
        name='quota_list__lib__work_order__uid',
        lookup_expr='exact')
    category = filters.NumberFilter(name='quota_list__category',
                                    lookup_expr='exact')

    class Meta:
        model = None
        fields = ('work_order_uid', 'category')


class PrincipalQuotaItemFilter(AbstractQuotaFilter):
    class Meta(AbstractQuotaFilter.Meta):
        model = PrincipalQuotaItem


class QuotaListFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(name='lib__work_order__uid',
                                        lookup_expr='exact')
    category = filters.NumberFilter(name='category', lookup_expr='exact')

    class Meta:
        fields = ('work_order_uid', 'category')
        model = QuotaList


class WeldingQuotaItemFilter(AbstractQuotaFilter):
    class Meta(AbstractQuotaFilter.Meta):
        model = WeldingQuotaItem


class MaterialFilter(filters.FilterSet):
    category = filters.ChoiceFilter(name='category', lookup_expr='exact',
                                    choices=MATERIAL_CATEGORY_CHOICES)

    class Meta:
        model = Material
        fields = ('category',)


class AuxiliaryQuotaItemFilter(AbstractQuotaFilter):
    class Meta(AbstractQuotaFilter.Meta):
        model = AuxiliaryQuotaItem


class WeldingSeamFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(
        name='process_material__lib__work_order__uid', lookup_expr='exact')

    class Meta:
        model = WeldingSeam
        fields = ('work_order_uid',)


class TotalWeldingMaterialFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(method='filter_work_order')

    class Meta:
        model = TotalWeldingMaterial
        fields = ('work_order_uid',)

    def filter_work_order(self, queryset, name, value):
        work_order = WorkOrder.objects.filter(uid=value)
        if not work_order:
            return self.Meta.model.objects.none()
        process_materials = ProcessMaterial.objects.filter(
            lib__work_order=work_order[0])
        return self.Meta.model.objects.filter(
            process_materials__in=process_materials)


class WeldingMaterialFilter(TotalWeldingMaterialFilter):

    class Meta(TotalWeldingMaterialFilter.Meta):
        model = WeldingMaterial


class FluxMaterialFilter(TotalWeldingMaterialFilter):

    class Meta(TotalWeldingMaterialFilter.Meta):
        model = FluxMaterial


class WeldingProcessSpecificationFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(name='work_order__uid')

    class Meta:
        model = WeldingProcessSpecification
        fields = ('work_order_uid',)


class WeldingJointProcessAnalysisFilter(filters.FilterSet):
    spec = filters.CharFilter(name='spec')

    class Meta:
        model = WeldingJointProcessAnalysis
        fields = ('spec',)


class WeldingCertificationFilter(filters.FilterSet):
    weld_method = filters.NumberFilter(name='weld_method')

    class Meta:
        model = WeldingCertification
        fields = ('weld_method',)


class WeldingWorkInstructionFilter(filters.FilterSet):
    work_order_uid = filters.CharFilter(name='detail__spec__work_order__uid')

    class Meta:
        model = WeldingWorkInstruction
        fields = ('work_order_uid',)
