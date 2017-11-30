from rest_framework import viewsets, mixins

from Core.utils.pagination import SmallResultsSetPagination
from Distribution.models import Product, BiddingDocument
from Distribution.serializers import (ProductSerializer,
                                      BiddingDocumentSerializer)


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    产品API
    """
    serializer_class = ProductSerializer
    pagination_class = SmallResultsSetPagination
    queryset = Product.objects.all().order_by('-pk')


class BiddingDocumentViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    招标文件API
    """
    serializer_class = BiddingDocumentSerializer
    queryset = BiddingDocument.objects.all().order_by('-pk')
