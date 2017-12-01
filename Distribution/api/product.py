from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from Core.utils.pagination import SmallResultsSetPagination
from Distribution.models import Product, BiddingDocument
from Distribution import serializers


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = Product.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ProductCreateSerializer
        elif self.action == 'list':
            return serializers.ProductListSerializer
        else:
            return serializers.ProductSerializer

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)


class BiddingDocumentViewSet(viewsets.ModelViewSet):
    """
    招标文件API
    """
    pagination_class = SmallResultsSetPagination
    serializer_class = serializers.BiddingDocumentSerializer
    queryset = BiddingDocument.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BiddingDocumentCreateSerializer
        elif self.action == 'list':
            return serializers.BiddingDocumentListSerializer
        else:
            return serializers.BiddingDocumentSerializer

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)
