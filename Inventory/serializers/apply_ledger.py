from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialApplyCard,
    SteelMaterialApplyDetail,
    AuxiliaryMaterialApplyCard,
    BoughtInComponentApplyDetail,
)


class WeldingMaterialApplyLedgerSerializer(serializers.ModelSerializer):
    sub_order_uid = serializers.CharField(
        source='sub_order.uid')
    # TODO: Replace with true field
    welding_seam_uid = serializers.CharField(default='')
    apply_dt = serializers.DateTimeField(source='create_dt')
    applicant = serializers.CharField(source='applicant.first_name')
    apply_card_uid = serializers.CharField(source='uid')

    class Meta:
        model = WeldingMaterialApplyCard
        fields = ('id', 'sub_order_uid', 'welding_seam_uid', 'apply_dt',
                  'applicant', 'department', 'apply_card_uid', 'actual_weight',
                  'actual_count')


class SteelMaterialApplyLedgerSerializer(serializers.ModelSerializer):
    sub_order_uid = serializers.CharField(
        source='apply_card.sub_order.uid')
    material = serializers.CharField(
        source='procurement_material.process_material.material.name')
    specification = serializers.CharField(
        source='procurement_material.process_material.spec')
    apply_dt = serializers.CharField(source='apply_card.create_dt')
    material_number = serializers.CharField(
        source='procurement_material.process_material.material.uid')
    apply_count = serializers.IntegerField(source='count')

    class Meta:
        model = SteelMaterialApplyDetail
        fields = ('id', 'sub_order_uid', 'material', 'specification',
                  'apply_dt', 'material_number', 'apply_count')


class AuxiliaryMaterialApplyLedgerSerializer(serializers.ModelSerializer):
    apply_name = serializers.CharField(
        source=('apply_inventory.entry_detail.procurement_material'
                '.process_material.name'))
    apply_specification = serializers.CharField(
        source=('apply_inventory.entry_detail.procurement_material'
                '.process_material.spec'))
    apply_card_uid = serializers.CharField(source='uid')
    apply_dt = serializers.CharField(source='create_dt')
    actual_specification = serializers.CharField(
        source=('actual_inventory.entry_detail.procurement_material'
                '.process_material.spec'), default='')

    class Meta:
        model = AuxiliaryMaterialApplyCard
        fields = ('id', 'department', 'apply_name', 'apply_specification',
                  'apply_count', 'apply_card_uid', 'apply_dt',
                  'actual_specification', 'actual_count')


class BoughtInComponentApplyLedgerSerializer(serializers.ModelSerializer):
    sub_order_uid = serializers.CharField(
        source='apply_card.sub_order.uid')
    material = serializers.CharField(
        source='procurement_material.process_material.material.name')
    specification = serializers.CharField(
        source='procurement_material.process_material.spec')
    apply_dt = serializers.CharField(source='apply_card.create_dt')
    material_number = serializers.CharField(
        source='procurement_material.process_material.material.uid')
    apply_card_uid = serializers.CharField(source='apply_card.uid')
    apply_count = serializers.IntegerField(source='count')

    class Meta:
        model = BoughtInComponentApplyDetail
        fields = ('id', 'sub_order_uid', 'specification', 'material',
                  'apply_dt', 'material_number', 'apply_card_uid',
                  'apply_count')
