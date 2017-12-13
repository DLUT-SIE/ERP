from rest_framework import serializers

from Core.models import WorkOrder, SubWorkOrder


class WorkOrderSerializer(serializers.ModelSerializer):
    pretty_sell_type = serializers.CharField(source='get_sell_type_display',
                                             read_only=True)

    class Meta:
        model = WorkOrder
        fields = '__all__'


class SubWorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubWorkOrder
        fields = '__all__'
