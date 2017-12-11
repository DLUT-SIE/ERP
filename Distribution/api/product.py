from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from Core.utils.pagination import SmallResultsSetPagination
from Distribution import serializers
from Distribution.filters import ProductFilter
from Distribution.models import Product, BiddingDocument


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = Product.objects.all().order_by('-pk')
    filter_class = ProductFilter

    def get_serializer_class(self):
        args = set(self.request.GET.keys())
        pagination_args = {'page', 'limit'}
        extra_args = args - pagination_args
        if self.action == 'create':
            return serializers.ProductCreateSerializer
        elif self.action == 'list':
            if not extra_args:
                return serializers.ProductListSerializer
            else:
                return serializers.ProductSimpleSerializer
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
