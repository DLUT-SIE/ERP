from rest_framework import serializers

from Inventory.models import (
    BoardSteelMaterialRefundDetail,
    BarSteelMaterialRefundDetail,
    BoughtInComponentRefundDetail,
)


class BoardSteelMaterialRefundDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(default='', read_only=True)
    material = serializers.CharField(
        source='apply_detail.procurement_material.process_material.material',
        read_only=True)
    material_code = serializers.CharField(
        source='apply_detail.procurement_material.material_number',
        read_only=True)
    apply_card_uid = serializers.CharField(source='apply_card.uid',
                                           read_only=True)

    class Meta:
        model = BoardSteelMaterialRefundDetail
        fields = ('id', 'name', 'material', 'specification', 'material_code',
                  'status', 'count', 'weight', 'apply_card_uid')


class BarSteelMaterialRefundDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(default='', read_only=True)
    material = serializers.CharField(
        source='apply_detail.procurement_material.process_material.material',
        read_only=True)
    material_code = serializers.CharField(
        source='apply_detail.procurement_material.material_number',
        read_only=True)
    apply_card_uid = serializers.CharField(source='apply_card.uid',
                                           read_only=True)

    class Meta:
        model = BarSteelMaterialRefundDetail
        fields = ('id', 'name', 'material', 'specification', 'material_code',
                  'status', 'count', 'weight', 'apply_card_uid')


class BoughtInComponentRefundDetailSerializer(serializers.ModelSerializer):
    drawing_number = serializers.CharField(
        source=('apply_detail.procurement_material'
                '.process_material.drawing_number'),
        read_only=True)
    specification = serializers.CharField(
        source='apply_detail.procurement_material.spec',
        read_only=True, default='')
    name = serializers.CharField(
        source='apply_detail.procurement_material.process_material.name',
        read_only=True)
    material_number = serializers.CharField(
        source='apply_detail.procurement_material.material_number',
        read_only=True)
    unit = serializers.CharField(
        source='apply_detail.inventory_detail.entry_detail.unit',
        read_only=True)

    class Meta:
        model = BoughtInComponentRefundDetail
        fields = ('id', 'drawing_number', 'specification', 'name', 'unit',
                  'count', 'material_number', 'remark')
