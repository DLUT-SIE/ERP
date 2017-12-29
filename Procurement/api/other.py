
from rest_framework import viewsets
from Core.utils.pagination import SmallResultsSetPagination
from Procurement import serializers
from Procurement import models


# 过程跟踪
class ProcessFollowingInfoViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = models.ProcessFollowingInfo.objects.all().order_by('-pk')
    serializer_class = serializers.BaseProcessFollowingInfoSerializer


# 到货检验
class ArrivalInspectionViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = models.ArrivalInspection.objects.all().order_by('-pk')
    serializer_class = serializers.BaseArrivalInspectionSerializer
