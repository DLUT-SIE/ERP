from rest_framework import serializers

from Core.models import WorkOrder, SubWorkOrder


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'


class SubWorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubWorkOrder
        fields = '__all__'
