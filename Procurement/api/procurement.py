from rest_framework import viewsets
from Core.utils.pagination import SmallResultsSetPagination
from Procurement.models import PurchaseOrder, ProcurementMaterial
from Procurement import serializers
from Procurement.filters import (PurchaseOrderFilter,
                                 ProcurementMaterialFilter)


# 采购单
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = PurchaseOrder.objects.all().order_by('-pk')
    filter_class = PurchaseOrderFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PurchaseOrderListSerializer
        elif self.action == 'create':
            return serializers.PurchaseOrderCreateSerializer
        else:
            return serializers.PurchaseOrderReadSerializer


# 采购物料
class ProcurementMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcurementMaterial.objects.all().order_by('-pk')
    filter_class = ProcurementMaterialFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProcurementMaterialListSerializer
        elif self.action == 'create':
            return serializers.BaseProcurementMaterialSerializer
        else:
            return serializers.ProcurementMaterialReadSerializer
