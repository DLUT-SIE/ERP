from rest_framework import serializers
from django.db.models import Sum
from Procurement.models import ContractDetail


class ContractDetailSerializer(serializers.ModelSerializer):
    contract_number = serializers.CharField(
        source='bidding_sheet.contract_number', read_only=True)
    contract_amount = serializers.FloatField(
        source='bidding_sheet.contract_amount', read_only=True)
    billing_amount = serializers.FloatField(
        source='bidding_sheet.billing_amount', read_only=True)
    accept_supplier = serializers.CharField(
        source='bidding_sheet.biddingacceptance.accept_supplier',
        read_only=True)
    content = serializers.CharField(
        source='bidding_sheet.biddingacceptance.content',
        read_only=True)
    prepaid_amount = serializers.SerializerMethodField(read_only=True)
    payable_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContractDetail
        fields = '__all__'
        read_only_fields = ('submitter',)

    @staticmethod
    def get_sum(obj):
        if not hasattr(obj, 'sum'):
            obj.sum = obj.bidding_sheet.contractdetail_set.aggregate(
                Sum('amount'))['amount__sum']
        return obj.sum

    def get_prepaid_amount(self, obj):
        return self.get_sum(obj)

    def get_payable_amount(self, obj):
        return obj.bidding_sheet.billing_amount - self.get_sum(obj)
