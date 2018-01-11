from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import MaterialSubApply, MaterialSubApplyItems
from Procurement.models import SubApplyComment
from Procurement import serializers
from Procurement import filters


# 材料代用申请单
class MaterialSubApplyViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = MaterialSubApply.objects.all().order_by('-pk')
    filter_class = filters.MaterialSubApplyFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MaterialSubApplyListSerializer
        elif self.action == "update":
            return serializers.MaterialSubApplyUpdateSerializer
        else:
            return serializers.MaterialSubApplySerializer

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)


# 材料代用申请单明细
class MaterialSubApplyItemViewSet(viewsets.ModelViewSet):
    queryset = MaterialSubApplyItems.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.MaterialSubApplyItemsUpdateSerializer
        else:
            return serializers.MaterialSubApplyItemsSerializer


# 材料代用申请单评论
class MaterialSubApplyCommentViewSet(viewsets.ModelViewSet):
    queryset = SubApplyComment.objects.all().order_by('-pk')
    serializer_class = serializers.MaterialSubApplyCommentsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
