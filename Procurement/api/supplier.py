from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import (Supplier, SupplierDocument, Quotation,
                                SupplyRelationship, SupplierCheck)
from Procurement import serializers
from Procurement import filters


# 供应商
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


# 供应商文件
class SupplierDocumentViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SupplierDocument.objects.all().order_by('-pk')
    serializer_class = serializers.SupplierDocumentSerializer


# 供应商报价单
class QuotationViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = Quotation.objects.all().order_by('-pk')
    serializer_class = serializers.QuotationSerializer


# 供应商标单关系
class SupplyRelationshipViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SupplyRelationship.objects.all().order_by('-pk')
    filter_class = filters.SupplyRelationshipFilter
    serializer_class = serializers.BaseSupplyRelationshipSerializer


# 供应商审核
class SupplierCheckViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SupplierCheck.objects.all().order_by('-pk')
    serializer_class = serializers.BaseSupplierCheckSerializer
