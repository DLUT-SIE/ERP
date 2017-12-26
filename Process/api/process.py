from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from Core.utils.pagination import SmallResultsSetPagination
from Process.models import (
    ProcessLibrary, ProcessMaterial, CirculationRoute, BoughtInItem, QuotaList,
    ProcessRoute, TransferCard, TransferCardProcess, FirstFeedingItem,
    CooperantItem, PrincipalQuotaItem)
from Process.serializers import (
    ProcessLibrarySerializer, ProcessMaterialSerializer,
    TransferCardSerializer, CirculationRouteSerializer, ProcessRouteSerializer,
    TransferCardListSerializer, TransferCardProcessSerializer,
    BoughtInItemSerializer, BoughtInItemUpdateSerializer, QuotaListSerializer,
    FirstFeedingItemUpdateSerializer, FirstFeedingItemSerializer,
    CooperantItemUpdateSerializer, CooperantItemSerializer,
    PrincipalQuotaItemSerializer)
from Process.filters import (
    ProcessLibraryFilter, ProcessMaterialFilter, CirculationRouteFilter,
    ProcessRouteFilter, TransferCardFilter, TransferCardProcessFilter,
    BoughtInItemFilter, FirstFeedingItemFilter, CooperantItemFilter,
    PrincipalQuotaItemFilter, QuotaListFilter)


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
    serializer_class = PrincipalQuotaItemSerializer


class QuotaListViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = QuotaList.objects.all().order_by('-pk')
    filter_class = QuotaListFilter
    serializer_class = QuotaListSerializer
