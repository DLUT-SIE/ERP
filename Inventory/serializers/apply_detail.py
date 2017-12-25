from rest_framework import serializers

from Inventory.models import (
    SteelMaterialApplyDetail,
    BoughtInComponentApplyDetail,
)


class SteelMaterialApplyDetailSerializer(serializers.ModelSerializer):
    sub_order_uid = serializers.CharField(source='sub_order.uid',
                                          read_only=True, default='')
    material_mark = serializers.CharField(
        source='process_material.name', read_only=True)
    # TODO: Review this field
    material_code = serializers.CharField(default='', read_only=True)
    specification = serializers.CharField(source='process_material.spec',
                                          read_only=True, default='')

    class Meta:
        model = SteelMaterialApplyDetail
        fields = ('id', 'sub_order_uid', 'material_mark', 'material_code',
                  'specification', 'count', 'component')


class BoughtInComponentApplyDetailSerializer(serializers.ModelSerializer):
    drawing_number = serializers.CharField(
        source='process_material.drawing_number',
        read_only=True)
    specification = serializers.CharField(source='process_material.spec',
                                          read_only=True, default='')
    name = serializers.CharField(
        source='process_material.name', read_only=True)
    # TODO: Review this field
    material_number = serializers.CharField(default='', read_only=True)

    class Meta:
        model = BoughtInComponentApplyDetail
        fields = ('id', 'drawing_number', 'specification', 'name', 'count',
                  'material_number', 'remark')
