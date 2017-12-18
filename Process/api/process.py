from rest_framework import viewsets
from django_filters import rest_framework as filters


from Core.utils.pagination import SmallResultsSetPagination
from Process.models import ProcessLibrary, ProcessMaterial
from Process.serializers import (
    ProcessLibrarySerializer, ProcessMaterialSerializer)
from Process.filters import ProcessLibraryFilter, ProcessMaterialFilter


class ProcessLibraryViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessLibrary.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProcessLibraryFilter
    serializer_class = ProcessLibrarySerializer


class ProcessMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessMaterial.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProcessMaterialFilter
    serializer_class = ProcessMaterialSerializer
