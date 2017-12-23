from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Production import serializers
from Production.models import ProcessDetail, SubMaterial
from Production.filters import ProcessDetailFilter


class ProcessDetailViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessDetail.objects.all().order_by('-pk')
    filter_class = ProcessDetailFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ProcessDetailCreateSerializer
        elif self.action == 'list':
            return serializers.ProcessDetailListSerializer
        else:
            return serializers.ProcessDetailSerializer


class SubMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SubMaterial.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.SubMaterialCreateSerializer
        else:
            return serializers.SubMaterialSerializer
