from django_filters import rest_framework as filters
from Procurement import models


class SupplyRelationshipFilter(filters.FilterSet):
    supplier_code = filters.CharFilter(name='supplier_code',
                                       lookup_expr='icontains')
    status = filters.CharFilter(name='status', lookup_expr='exact')
    supplier = filters.CharFilter(name="supplier", lookup_expr='icontains')

    class Meta:
        model = models.SupplyRelationship
        fields = ('status', 'bidding_sheet', 'supplier', 'supplier_code')


class SupplierFilter(filters.FilterSet):
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')

    class Meta:
        model = models.Supplier
        fields = ('uid',)


class SupplyDocumentFilter(filters.FilterSet):

    class Meta:
        model = models.SupplierDocument
        fields = ('supplier',)


class SupplyQuotationFilter(filters.FilterSet):

    class Meta:
        model = models.Quotation
        fields = ('supplier',)
