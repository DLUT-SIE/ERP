from rest_framework import viewsets, mixins
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
        # TODO: Why crash on /api?
        args = set(self.request.GET.keys()) if self.request else set()
        pagination_args = {'page', 'limit'}
        extra_args = args - pagination_args
        if self.action == 'create':
            return serializers.ProductCreateSerializer
        elif self.action == 'list':
            if not extra_args:
                return serializers.ProductListSerializer
            else:
                return serializers.ProductSimpleSerializer
        elif self.action == 'partial_update' or self.action == 'update':
            return serializers.ProductUpdateSerializer
        else:
            return serializers.ProductSerializer

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)


class BiddingDocumentViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    招标文件API
    """
    queryset = BiddingDocument.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action in ('partial_update', 'update'):
            return serializers.BiddingDocumentUpdateSerializer
        else:
            return serializers.BiddingDocumentSerializer
