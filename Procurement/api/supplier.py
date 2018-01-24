from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

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
    filter_class = filters.SupplierFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SupplierListSerializer
        elif self.action == "retrieve":
            return serializers.SupplierDetailSerializer
        else:
            return serializers.SupplierSerializer

    @list_route()
    def bidding_sheet(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        context = self.get_serializer_context()
        if page is not None:
            serializer = serializers.SupplierBiddingListSerializer(
                page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.SupplierBiddingListSerializer(
            queryset, many=True, context=context)
        return Response(serializer.data)


# 供应商文件
class SupplierDocumentViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SupplierDocument.objects.all().order_by('-pk')
    serializer_class = serializers.SupplierDocumentSerializer
    filter_class = filters.SupplyDocumentFilter


# 供应商报价单
class QuotationViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = Quotation.objects.all().order_by('-pk')
    serializer_class = serializers.QuotationSerializer
    filter_class = filters.SupplyQuotationFilter


# 供应商标单关系
class SupplyRelationshipViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SupplyRelationship.objects.all().order_by('-pk')
    filter_class = filters.SupplyRelationshipFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.SupplyRelationshipCreateSerializer
        else:
            return serializers.BaseSupplyRelationshipSerializer

    @list_route()
    def reset(self, request, *args, **kwargs):
        self.filter_queryset(self.get_queryset()).delete()
        return Response({'status': '供应商已重置'})


# 供应商审核
class SupplierCheckViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SupplierCheck.objects.all().order_by('-pk')
    serializer_class = serializers.BaseSupplierCheckSerializer
