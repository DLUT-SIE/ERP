from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from Core.utils.pagination import SmallResultsSetPagination
from Process.models import (
    ProcessLibrary, ProcessMaterial, CirculationRoute, BoughtInItem, QuotaList,
    ProcessRoute, TransferCard, TransferCardProcess, FirstFeedingItem,
    CooperantItem, PrincipalQuotaItem, WeldingQuotaItem, Material,
    AuxiliaryQuotaItem, WeldingSeam, TotalWeldingMaterial, WeldingMaterial,
    FluxMaterial)
from Process.serializers import (
    ProcessLibrarySerializer, ProcessMaterialSerializer,
    TransferCardSerializer, CirculationRouteSerializer, ProcessRouteSerializer,
    TransferCardListSerializer, TransferCardProcessSerializer,
    BoughtInItemSerializer, BoughtInItemUpdateSerializer, QuotaListSerializer,
    FirstFeedingItemUpdateSerializer, FirstFeedingItemSerializer,
    CooperantItemUpdateSerializer, CooperantItemSerializer,
    PrincipalQuotaItemSerializer, WeldingQuotaItemSerializer,
    PrincipalQuotaItemCreateSerializer, WeldingQuotaItemCreateSerializer,
    MaterialSerializer, AuxiliaryQuotaItemListSerializer,
    AuxiliaryQuotaItemSerializer, AuxiliaryQuotaItemCreateSerializer,
    WeldingSeamSerializer, WeldingSeamListSerializer,
    TotalWeldingMaterialSerializer, WeldingMaterialSerializer,
    FluxMaterialSerializer)
from Process.filters import (
    ProcessLibraryFilter, ProcessMaterialFilter, CirculationRouteFilter,
    ProcessRouteFilter, TransferCardFilter, TransferCardProcessFilter,
    BoughtInItemFilter, FirstFeedingItemFilter, CooperantItemFilter,
    PrincipalQuotaItemFilter, QuotaListFilter, WeldingQuotaItemFilter,
    MaterialFilter, AuxiliaryQuotaItemFilter, WeldingSeamFilter,
    TotalWeldingMaterialFilter, WeldingMaterialFilter, FluxMaterialFilter)


class ProcessLibraryViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessLibrary.objects.all().order_by('-pk')
    filter_class = ProcessLibraryFilter
    serializer_class = ProcessLibrarySerializer


class ProcessMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessMaterial.objects.all().order_by('-pk')
    filter_class = ProcessMaterialFilter
    serializer_class = ProcessMaterialSerializer


class CirculationRouteViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = CirculationRoute.objects.all().order_by('-pk')
    filter_class = CirculationRouteFilter
    serializer_class = CirculationRouteSerializer


class ProcessRouteViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessRoute.objects.all().order_by('-pk')
    filter_class = ProcessRouteFilter
    serializer_class = ProcessRouteSerializer


class TransferCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = TransferCard.objects.all().order_by('-pk')
    filter_class = TransferCardFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return TransferCardListSerializer
        else:
            return TransferCardSerializer


class TransferCardProcessViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    queryset = TransferCardProcess.objects.all().order_by('index')
    filter_class = TransferCardProcessFilter
    serializer_class = TransferCardProcessSerializer


class BoughtInItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = BoughtInItem.objects.all().order_by('-pk')
    filter_class = BoughtInItemFilter

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return BoughtInItemUpdateSerializer
        else:
            return BoughtInItemSerializer


class FirstFeedingItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = FirstFeedingItem.objects.all().order_by('-pk')
    filter_class = FirstFeedingItemFilter

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return FirstFeedingItemUpdateSerializer
        else:
            return FirstFeedingItemSerializer


class CooperantItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = CooperantItem.objects.all().order_by('-pk')
    filter_class = CooperantItemFilter

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CooperantItemUpdateSerializer
        else:
            return CooperantItemSerializer


class PrincipalQuotaItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = PrincipalQuotaItem.objects.all().order_by('-pk')
    filter_class = PrincipalQuotaItemFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return PrincipalQuotaItemCreateSerializer
        else:
            return PrincipalQuotaItemSerializer


class QuotaListViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = QuotaList.objects.all().order_by('-pk')
    filter_class = QuotaListFilter
    serializer_class = QuotaListSerializer


class WeldingQuotaItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingQuotaItem.objects.all().order_by('-pk')
    filter_class = WeldingQuotaItemFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return WeldingQuotaItemCreateSerializer
        else:
            return WeldingQuotaItemSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = Material.objects.all().order_by('-pk')
    filter_class = MaterialFilter
    serializer_class = MaterialSerializer


class AuxiliaryQuotaItemViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = AuxiliaryQuotaItem.objects.all().order_by('-pk')
    filter_class = AuxiliaryQuotaItemFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return AuxiliaryQuotaItemListSerializer
        elif self.action == 'create':
            return AuxiliaryQuotaItemCreateSerializer
        return AuxiliaryQuotaItemSerializer


class WeldingSeamViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingSeam.objects.all().order_by('-pk')
    filter_class = WeldingSeamFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return WeldingSeamListSerializer
        return WeldingSeamSerializer


class TotalWeldingMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = TotalWeldingMaterial.objects.all().order_by('-pk')
    filter_class = TotalWeldingMaterialFilter
    serializer_class = TotalWeldingMaterialSerializer


class WeldingMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = WeldingMaterial.objects.all().order_by('-pk')
    filter_class = WeldingMaterialFilter
    serializer_class = WeldingMaterialSerializer


class FluxMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = FluxMaterial.objects.all().order_by('-pk')
    filter_class = FluxMaterialFilter
    serializer_class = FluxMaterialSerializer
