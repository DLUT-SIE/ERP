from django_filters import rest_framework as filters
from Procurement import models
from Procurement import BIDDING_SHEET_STATUS_CHOICES


# 根据标单编号模糊查询
class BiddingSheetFilter(filters.FilterSet):
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')
    status = filters.MultipleChoiceFilter(
        name='status', choices=BIDDING_SHEET_STATUS_CHOICES)

    class Meta:
        model = models.BiddingSheet
        fields = ('uid', 'status')


class BiddingApplicationFilter(filters.FilterSet):
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')
    status = filters.ChoiceFilter(name='status', lookup_expr='exact')

    class Meta:
        model = models.BiddingApplication
        fields = ('uid', 'status')


class BiddingAcceptanceFilter(filters.FilterSet):
    bidding_sheet = filters.CharFilter(name='bidding_sheet',
                                       lookup_expr='exact')
    
    class Meta:
        model = models.BiddingAcceptance
        fields = ('bidding_sheet',)
