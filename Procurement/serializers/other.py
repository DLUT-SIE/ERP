from rest_framework import serializers
from Procurement import models


class BaseProcessFollowingInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProcessFollowingInfo
        fields = ('id', 'bidding_sheet', 'following_dt', 'following_method',
                  'following_feedback', 'path', 'executor', 'inform_process')


class BaseArrivalInspectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArrivalInspection
        fields = ('id', 'material', 'material_confirm', 'soft_confirm',
                  'inspection_confirm', 'passed')
