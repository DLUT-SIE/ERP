from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Production.models import ProcessDetail
from Production import serializers
from Production.filters import ManHourMessageFilter


class ManHourMessageViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessDetail.objects.all().order_by('-pk')
    filter_class = ManHourMessageFilter
    serializer_class = serializers.ManHourMessageSerializer
