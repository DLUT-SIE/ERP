from rest_framework import serializers

from Procurement.models import ContractDetail


class ContractDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContractDetail
        fields = '__all__'
        read_only_fields = ('submitter',)
