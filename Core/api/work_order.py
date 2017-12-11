from rest_framework import viewsets, mixins

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


class SubWorkOrderViewSet(mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    子工作令API
    """
    serializer_class = SubWorkOrderSerializer
    pagination_class = SmallResultsSetPagination
    queryset = SubWorkOrder.objects.all().order_by('-pk')
    filter_class = SubWorkOrderFilter
