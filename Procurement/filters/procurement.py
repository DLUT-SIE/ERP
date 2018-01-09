from django_filters import rest_framework as filters

from Procurement.models import (PurchaseOrder, ProcurementMaterial)
from Procurement import PURCHASE_ORDER_STATUS_CHOICES


class PurchaseOrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(name='status', lookup_expr='exact',
                                  choices=PURCHASE_ORDER_STATUS_CHOICES)
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')

    class Meta:
        model = PurchaseOrder
        fields = ('status', 'uid')


class ProcurementMaterialFilter(filters.FilterSet):

    purchase_order = filters.CharFilter(name='purchase_order',
                                        lookup_expr='exact')

    class Meta:
        model = ProcurementMaterial
        fields = ('purchase_order',)
