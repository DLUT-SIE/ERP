from rest_framework import viewsets
from Core.utils.pagination import SmallResultsSetPagination
from Procurement import serializers
from Procurement import models
from Procurement import filters


# 标单
class BiddingSheetViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = models.BiddingSheet.objects.all().order_by('-pk')
    filter_class = filters.BiddingSheetFilter

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'list':
            return serializers.BiddingSheetListSerializer
        elif self.action == 'retrieve':
            print("####")
            return serializers.BiddingSheetReadSerializer
        return serializers.BaseBiddingSheetSerializer


# 招标申请
class BiddingApplicationViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = models.BiddingApplication.objects.all().order_by('-pk')
    filter_class = filters.BiddingApplicationFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.BiddingApplicationCreateSerializer
        elif self.action == 'list':
            return serializers.BiddingApplicationListSerializer
        else:
            return serializers.BaseBiddingApplicationSerializer


# 中标通知书
class BiddingAcceptanceViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = models.BiddingAcceptance.objects.all().order_by('-pk')
    serializer_class = serializers.BaseBiddingAcceptanceSerializer
    filter_class = filters.BiddingAcceptanceFilter


# 比质比价卡
class ParityRatioCardViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = models.ParityRatioCard.objects.all().order_by('-pk')
    serializer_class = serializers.BaseParityRatioCardSerializer
