from rest_framework import serializers

from Procurement.models import ContractDetail


class ContractDetailSerializer(serializers.ModelSerializer):
    contract_number = serializers.CharField(
        source='bidding_sheet.contract_number', read_only=True)
    contract_amount = serializers.FloatField(
        source='bidding_sheet.contract_amount', read_only=True)
    billing_amount = serializers.FloatField(
        source='bidding_sheet.billing_amount', read_only=True)

    class Meta:
        model = ContractDetail
        fields = '__all__'
        read_only_fields = ('submitter',)
