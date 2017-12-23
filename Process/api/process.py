from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Process.models import (
    ProcessLibrary, ProcessMaterial, CirculationRoute,
    ProcessRoute, TransferCard)
from Process.serializers import (
    ProcessLibrarySerializer, ProcessMaterialSerializer,
    TransferCardSerializer, CirculationRouteSerializer, ProcessRouteSerializer,
    TransferCardListSerializer)
from Process.filters import (
    ProcessLibraryFilter, ProcessMaterialFilter, CirculationRouteFilter,
    ProcessRouteFilter, TransferCardFilter)


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
