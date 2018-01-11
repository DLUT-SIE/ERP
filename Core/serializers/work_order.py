from rest_framework import serializers

from Core.models import WorkOrder, SubWorkOrder


class WorkOrderSerializer(serializers.ModelSerializer):
    pretty_sell_type = serializers.CharField(source='get_sell_type_display',
                                             read_only=True)

    class Meta:
        model = WorkOrder
        fields = ('id', 'uid', 'sell_type', 'pretty_sell_type',
                  'client', 'project', 'product', 'count', 'finished')


class SubWorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubWorkOrder
        fields = ('id', 'work_order', 'index', 'finished')
