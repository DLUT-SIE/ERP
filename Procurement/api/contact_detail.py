from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import ContractDetail
from Procurement import serializers


class ContractDetailViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ContractDetail.objects.all().order_by('-pk')
    serializer_class = serializers.ContractDetailSerializer

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user,)
