from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Production import serializers
from Production.models import ProductionUser, ProductionWorkGroup
from Production.filters import (ProductionUserFilter,
                                ProductionWorkGroupFilter)


class ProductionWorkGroupViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProductionWorkGroup.objects.all().order_by('-pk')
    filter_class = ProductionWorkGroupFilter
    serializer_class = serializers.ProductionWorkGroupSerializer


class ProductionUserViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProductionUser.objects.all().order_by('-pk')
    filter_class = ProductionUserFilter

    def get_serializer_class(self):
        if self.action in ('partial_update', 'update'):
            return serializers.ProductionUserUpdateSerializer
        else:
            return serializers.ProductionUserSerializer
