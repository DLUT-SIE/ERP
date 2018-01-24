from rest_framework import serializers

from Inventory.models import (
    Warehouse,
    WeldingMaterialHumitureRecord,
    WeldingMaterialBakeRecord,
)


class WarehouseSerializer(serializers.ModelSerializer):
    pretty_category = serializers.CharField(source='get_category_display',
                                            read_only=True)

    class Meta:
        model = Warehouse
        fields = ('id', 'name', 'location', 'category', 'pretty_category')


class WeldingMaterialHumitureRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldingMaterialHumitureRecord
        fields = ('id', 'create_dt', 'keeper', 'actual_temp_1',
                  'actual_humid_1', 'actual_temp_2', 'actual_humid_2',
                  'remark')
        read_only_fields = ('keeper',)


class WeldingMaterialHumitureRecordListSerializer(
        WeldingMaterialHumitureRecordSerializer):
    class Meta(WeldingMaterialHumitureRecordSerializer.Meta):
        fields = ('id', 'create_dt', 'keeper')


class WeldingMaterialBakeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldingMaterialBakeRecord
        fields = ('id', 'create_dt', 'standard_num', 'size', 'class_num',
                  'heat_num', 'codedmark', 'quantity', 'furnace_time',
                  'baking_temp', 'heating_time', 'cooling_time',
                  'holding_time', 'holding_temp', 'apply_time', 'keeper',
                  'welding_engineer', 'remark')


class WeldingMaterialBakeRecordListSerializer(
        WeldingMaterialBakeRecordSerializer):
    class Meta(WeldingMaterialBakeRecordSerializer.Meta):
        fields = ('id', 'create_dt', 'standard_num', 'size', 'heat_num',
                  'codedmark', 'keeper', 'welding_engineer')
