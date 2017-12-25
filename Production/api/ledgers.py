from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from Core.utils.pagination import SmallResultsSetPagination
from Production import serializers
from Production.models import SubMaterial
from Production.filters import SubMaterialLedgersFilter


class SubMaterialLedgersViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SubMaterial.objects.all().order_by('-pk')
    filter_class = SubMaterialLedgersFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SubMaterialLedgersListSerializer
        else:
            return serializers.SubMaterialLedgersUpdateSerializer

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)
