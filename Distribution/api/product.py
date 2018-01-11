from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.exceptions import MethodNotAllowed

from Core.models import Department
from Core.utils.pagination import SmallResultsSetPagination
from Distribution import serializers
from Distribution.filters import ProductFilter
from Distribution.models import Product, BiddingDocument


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = (Product.objects.all().order_by('-pk')
                .prefetch_related('documents'))
    filter_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ProductCreateSerializer
        elif self.action == 'list':
            if 'department' in self.request.GET:
                return serializers.ProductSimpleSerializer
            else:
                return serializers.ProductListSerializer
        elif self.action in ('partial_update', 'update'):
            return serializers.ProductUpdateSerializer
        else:
            return serializers.ProductSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request and 'department' in self.request.GET:
            dep_id = self.request.GET['department']
            context['department'] = get_object_or_404(Department, id=dep_id)
        return context

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
