from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from Core.utils.pagination import SmallResultsSetPagination
from Production.models import ProductionPlan
from Production import serializers
from Production.filters import ProductionPlanFilter


class ProductionPlanViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProductionPlan.objects.all().order_by('-pk')
    filter_class = ProductionPlanFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductionPlanListSerializer
        elif self.action == 'create':
            return serializers.ProductionPlanCreateSerializer
        else:
            return serializers.ProductionPlanUpdateSerializer

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)
