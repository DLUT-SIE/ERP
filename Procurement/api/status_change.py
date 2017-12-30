from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import StatusChange
from Procurement import serializers
from Procurement import filters


# 状态回溯
class StatusChangeViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = StatusChange.objects.all().order_by('-pk')
    serializer_class = serializers.StatusChangeSerializer
    filter_class = filters.StatusChangeFilter
