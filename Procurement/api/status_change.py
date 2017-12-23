from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import StatusChange
from Procurement import serializers


class StatusChangeViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = StatusChange.objects.all().order_by('-pk')
    serializer_class = serializers.StatusChangeSerializer

    def perform_create(self, serializer):
        serializer.save(change_user=self.request.user, normal_change=False)
