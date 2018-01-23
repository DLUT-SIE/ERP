from rest_framework import serializers
from Procurement import models
from Procurement.serializers import (BaseTransitionSerializer,
                                     BaseDynamicFieldSerializer)


# 标单
class BaseBiddingSheetSerializer(BaseTransitionSerializer):
    purchase_order_uid = serializers.CharField(source='purchase_order.uid',
                                               read_only=True)

    class Meta:
        model = models.BiddingSheet
        fields = ('id', 'uid', 'purchase_order', 'purchase_order_uid',
                  'create_dt', 'status', 'contract_amount', 'billing_amount',
                  'category')


class BiddingSheetListSerializer(BaseBiddingSheetSerializer):

    pretty_status = serializers.CharField(source='get_status_display')

    class Meta(BaseBiddingSheetSerializer.Meta):
        fields = ('id', 'uid', 'purchase_order', 'purchase_order_uid',
                  'create_dt', 'status', 'category', 'pretty_status')


# 标单申请表
class BaseBiddingApplicationSerializer(BaseTransitionSerializer):
    work_order_uid = serializers.CharField(source='work_order.uid',
                                           read_only=True)
    bidding_sheet_uid = serializers.CharField(source='bidding_sheet.uid',
                                              read_only=True)

    class Meta:
        model = models.BiddingApplication
        fields = ('id', 'uid', 'bidding_sheet', 'bidding_sheet_uid',
                  'applicant', 'requestor', 'amount', 'work_order',
                  'work_order_uid', 'plan_project', 'plan_dt', 'model',
                  'is_core_part', 'category', 'tender_dt', 'delivery_dt',
                  'place', 'status', 'implement_class')


class BiddingApplicationCreateSerializer(BaseBiddingApplicationSerializer):

    class Meta(BaseBiddingApplicationSerializer.Meta):
        read_only_fields = ('id', 'work_order', 'plan_project', 'plan_dt',
                            'model', 'category', 'tender_dt', 'delivery_dt',
                            'place')


class BiddingApplicationListSerializer(BaseBiddingApplicationSerializer):
    class Meta(BaseBiddingApplicationSerializer.Meta):
        fields = ('id', 'uid', 'bidding_sheet', 'bidding_sheet_uid',
                  'implement_class')


# 中标通知书
class BaseBiddingAcceptanceSerializer(BaseDynamicFieldSerializer):
    class Meta:
        model = models.BiddingAcceptance
        fields = ('id', 'uid', 'bidding_sheet', 'requestor', 'content',
                  'amount', 'accept_dt', 'accept_money', 'contact',
                  'contact_phone')


# 比质比价卡
class BaseParityRatioCardSerializer(BaseTransitionSerializer):
    class Meta:
        model = models.ParityRatioCard
        fields = ('id', 'bidding_sheet', 'apply_id', 'applicant', 'requestor',
                  'work_order', 'amount', 'unit', 'content', 'material',
                  'delivery_period', 'status')
