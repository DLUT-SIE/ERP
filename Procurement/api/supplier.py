from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import Supplier, SupplierDocument, Quotation
from Procurement import serializers


class SupplierViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = Supplier.objects.all().order_by('-pk')
    serializer_class = serializers.SupplierSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SupplierListSerializer
        elif self.action == "retrieve":
            return serializers.SupplierDetailSerializer
        else:
            return serializers.SupplierSerializer


class SupplierDocumentViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SupplierDocument.objects.all().order_by('-pk')
    serializer_class = serializers.SupplierDocumentSerializer


class QuotationViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = Quotation.objects.all().order_by('-pk')
    serializer_class = serializers.QuotationSerializer
