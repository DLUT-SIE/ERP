from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route

from Core.models import WorkOrder, SubWorkOrder
from Core.filters import SubWorkOrderFilter
from Core.serializers import WorkOrderSerializer, SubWorkOrderSerializer
from Core.utils.pagination import SmallResultsSetPagination


class WorkOrderViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    工作令API
    """
    serializer_class = WorkOrderSerializer
    pagination_class = SmallResultsSetPagination
    queryset = WorkOrder.objects.all().order_by('-pk')

    @list_route()
    def non_production_plans(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            productionplan__isnull=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class SubWorkOrderViewSet(mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    子工作令API
    """
    serializer_class = SubWorkOrderSerializer
    pagination_class = SmallResultsSetPagination
    queryset = (SubWorkOrder.objects.all().order_by('-pk')
                .select_related('work_order'))
    filter_class = SubWorkOrderFilter
