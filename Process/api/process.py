from rest_framework import viewsets
from django_filters import rest_framework as filters


from Core.utils.pagination import SmallResultsSetPagination
from Process.models import ProcessLibrary
from Process.serializers import (
    ProcessLibraryListSerializer,
    ProcessLibrarySerializer)
from Process.filters.process import ProcessLibraryFilter


class ProcessLibraryViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessLibrary.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProcessLibraryFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ProcessLibraryListSerializer
        else:
            return ProcessLibrarySerializer
