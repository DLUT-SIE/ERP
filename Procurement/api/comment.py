from rest_framework import viewsets
from Core.utils.pagination import SmallResultsSetPagination
from Procurement import serializers
from Procurement import models


# 标单评审意见
class BiddingCommentViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = models.BiddingComment.objects.all().order_by('-pk')
    serializer_class = serializers.BaseBiddingCommentSerializer
