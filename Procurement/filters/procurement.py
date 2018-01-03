from django_filters import rest_framework as filters

from Procurement.models import PurchaseOrder


class PurchaseOrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(name='status', lookup_expr='exact')
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')

    class Meta:
        model = PurchaseOrder
        fields = ('status', 'uid')
