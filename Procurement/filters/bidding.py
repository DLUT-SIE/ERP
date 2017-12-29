from django_filters import rest_framework as filters
from Procurement import models


# 根据标单编号模糊查询
class BiddingSheetFilter(filters.FilterSet):
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')
    status = filters.ChoiceFilter(name='status', lookup_expr='exact')

    class Meta:
        model = models.BiddingSheet
        fields = ('uid', 'status')


class BiddingApplicationFilter(filters.FilterSet):
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')
    status = filters.ChoiceFilter(name='status', lookup_expr='exact')

    class Meta:
        model = models.BiddingApplication
        fields = ('uid', 'status')
