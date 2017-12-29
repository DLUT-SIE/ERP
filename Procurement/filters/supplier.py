from django_filters import rest_framework as filters
from Procurement import models


class SupplyRelationshipFilter(filters.FilterSet):
    supplier_code = filters.CharFilter(name='supplier_code',
                                       lookup_expr='icontains')
    status = filters.CharFilter(name='status', lookup_expr='exact')
    bidding_sheet = filters.CharFilter(name='bidding_sheet',
                                       lookup_expr='icontains')
    supplier = filters.CharFilter(name="supplier", lookup_expr='icontains')

    class Meta:
        model = models.SupplyRelationship
        fields = ('status', 'bidding_sheet', 'supplier', 'supplier_code')
