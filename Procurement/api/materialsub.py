from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import MaterialSubApply, MaterialSubApplyItems
from Procurement.models import SubApplyComment
from Procurement import serializers


class MaterialSubApplyViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = MaterialSubApply.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.MaterialSubApplyCreateSerializer
        if self.action == 'list':
            return serializers.MaterialSubApplyListSerializer
        else:
            return serializers.MaterialSubApplySerializer

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)


class MaterialSubApplyItemsViewSet(viewsets.ModelViewSet):

    queryset = MaterialSubApplyItems.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.MaterialSubApplyItemsUpdateSerializer
        else:
            return serializers.MaterialSubApplyItemsSerializer


class MaterialSubApplyCommentsViewSet(viewsets.ModelViewSet):

    queryset = SubApplyComment.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.MaterialSubApplyCommentsCreateSerializer
        else:
            return serializers.MaterialSubApplyCommentsSerializer
