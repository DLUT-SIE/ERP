from rest_framework import viewsets

from Inventory.models import WeldingMaterialEntry
from Inventory import serializers


class WeldingMaterialEntryViewSet(viewsets.ModelViewSet):
    queryset = WeldingMaterialEntry.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.WeldingMaterialEntryListSerializer
        else:
            return serializers.WeldingMaterialEntrySerializer
