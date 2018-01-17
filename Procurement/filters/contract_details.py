from django_filters import rest_framework as filters

from Procurement.models import ContractDetail


class ContractDetailFilter(filters.FilterSet):

    class Meta:
        model = ContractDetail
        fields = ('bidding_sheet', )
