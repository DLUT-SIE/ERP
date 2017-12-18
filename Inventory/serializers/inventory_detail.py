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
        fields = '__all__'


class SteelMaterialInventoryDetailSerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    unit = serializers.CharField(source='entry_detail.unit', read_only=True)

    class Meta:
        model = SteelMaterialInventoryDetail
        fields = '__all__'


class AuxiliaryMaterialInventoryDetailSerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    unit = serializers.CharField(source='entry_detail.unit', read_only=True)

    class Meta:
        model = AuxiliaryMaterialInventoryDetail
        fields = '__all__'


class BoughtInComponentInventoryDetailSerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    unit = serializers.CharField(source='entry_detail.unit', read_only=True)

    class Meta:
        model = BoughtInComponentInventoryDetail
        fields = '__all__'
