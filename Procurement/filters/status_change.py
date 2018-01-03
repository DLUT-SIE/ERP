from django_filters import rest_framework as filters

from Procurement.models import StatusChange


class StatusChangeFilter(filters.FilterSet):

    class Meta:
        model = StatusChange
        fields = ('bidding_sheet', )
