from rest_framework import serializers
from django.db import transaction

from Procurement.models import StatusChange
from Procurement.models import BiddingSheet


class StatusChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatusChange
        fields = '__all__'
        read_only_fields = ('normal_change', 'change_user')

    def create(self, validated_data):
        with transaction.atomic():
            changelist = StatusChange(
                change_user=self.context['request'].user,
                normal_change=False,
                **validated_data)
            changelist.save()
            BiddingSheet.objects.filter(
                uid=validated_data['bidding_sheet']).update(
                status=validated_data['new_status'])
            return changelist
