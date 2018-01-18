from rest_framework import serializers
from Procurement.models import ContractDetail, BiddingSheet


class ContractSerializer(serializers.ModelSerializer):
    accept_supplier = serializers.CharField(
        source='biddingacceptance.accept_supplier',
        read_only=True)
    content = serializers.CharField(
        source='biddingacceptance.content',
        read_only=True)
    prepaid_amounts = serializers.FloatField(
        source='prepaid_amount',
        read_only=True)
    payable_amounts = serializers.FloatField(
        source='payable_amount',
        read_only=True)

    class Meta:
        model = BiddingSheet
        fields = ('id', 'uid', 'contract_number', 'contract_amount',
                  'billing_amount', 'accept_supplier', 'content',
                  'prepaid_amounts', 'payable_amounts')


class ContractDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractDetail
        fields = '__all__'
        read_only_fields = ('submitter',)

    def validate(self, data):
        if data['amount'] <= data['bidding_sheet'].payable_amount:
            return data
        else:
            raise serializers.ValidationError("Amout out of Range!")
