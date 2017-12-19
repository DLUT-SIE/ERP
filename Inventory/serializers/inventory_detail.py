from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialInventoryDetail,
    SteelMaterialInventoryDetail,
    AuxiliaryMaterialInventoryDetail,
    BoughtInComponentInventoryDetail)


class WeldingMaterialInventoryDetailSerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    unit = serializers.CharField(source='entry_detail.unit', read_only=True)

    class Meta:
        model = WeldingMaterialInventoryDetail
        fields = ('id', 'entry_detail', 'deadline', 'weight', 'count',
                  'unit', 'status', 'pretty_status')


class SteelMaterialInventoryDetailSerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    unit = serializers.CharField(source='entry_detail.unit', read_only=True)

    class Meta:
        model = SteelMaterialInventoryDetail
        fields = ('id', 'entry_detail', 'length', 'refund_times', 'weight',
                  'count', 'unit', 'status', 'pretty_status')


class AuxiliaryMaterialInventoryDetailSerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    unit = serializers.CharField(source='entry_detail.unit', read_only=True)

    class Meta:
        model = AuxiliaryMaterialInventoryDetail
        fields = ('id', 'entry_detail', 'weight',
                  'count', 'unit', 'status', 'pretty_status')


class BoughtInComponentInventoryDetailSerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    unit = serializers.CharField(source='entry_detail.unit', read_only=True)

    class Meta:
        model = BoughtInComponentInventoryDetail
        fields = ('id', 'entry_detail', 'weight',
                  'count', 'unit', 'status', 'pretty_status')
