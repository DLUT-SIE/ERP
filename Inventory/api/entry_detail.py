from rest_framework import viewsets

from Inventory.models import WeldingMaterialEntryDetail
from Inventory import serializers


class WeldingMaterialEntryDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WeldingMaterialEntryDetailSerializer
    queryset = WeldingMaterialEntryDetail.objects.all().order_by('-pk')
