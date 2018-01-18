from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import ContractDetail, BiddingSheet
from Procurement import serializers
from Procurement import filters


# 合同列表
class ContractViewset(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = BiddingSheet.objects.all().order_by('-pk')
    serializer_class = serializers.ContractSerializer


# 合同金额明细
class ContractDetailViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ContractDetail.objects.all().order_by('-pk')
    serializer_class = serializers.ContractDetailSerializer
    filter_class = filters.ContractDetailFilter

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user,)
