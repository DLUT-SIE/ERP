from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialInventoryDetail, SteelMaterialInventoryDetail,
    AuxiliaryMaterialInventoryDetail, BoughtInComponentInventoryDetail)


class WeldingMaterialInventoryLedgerSerializer(serializers.ModelSerializer):
    material_mark = serializers.CharField(
        source='entry_detail.procurement_material.process_material.name',
        allow_null=True, read_only=True)
    specification = serializers.CharField(
        source='entry_detail.procurement_material.process_material.spec',
        allow_null=True, read_only=True)
    entry_count = serializers.FloatField(source='entry_detail.count')
    entry_dt = serializers.DateTimeField(
        source='entry_detail.entry.create_dt')
    material_number = serializers.CharField(
        source=('entry_detail.procurement_material.'
                'process_material.material.uid'),
        allow_null=True, read_only=True)
    factory = serializers.CharField(source='entry_detail.factory')
    pretty_status = serializers.CharField(source='get_status_display')

    class Meta:
        model = WeldingMaterialInventoryDetail
        fields = ('id', 'material_mark', 'specification', 'entry_count',
                  'entry_dt', 'material_number', 'factory', 'count',
                  'pretty_status')


class SteelMaterialInventoryLedgerSerializer(serializers.ModelSerializer):
    material = serializers.CharField(
        source=('entry_detail.procurement_material'
                '.process_material.material.name'),
        allow_null=True, read_only=True)
    batch_number = serializers.CharField(
        source='entry_detail.procurement_material.batch_number',
        allow_null=True, read_only=True)
    specification = serializers.CharField(
        source='entry_detail.procurement_material.process_material.spec',
        allow_null=True, read_only=True)
    entry_dt = serializers.DateTimeField(
        source='entry_detail.entry.create_dt')
    material_number = serializers.CharField(
        source=('entry_detail.procurement_material.'
                'process_material.material.uid'),
        allow_null=True, read_only=True)
    work_order_uid = serializers.CharField(
        source='entry_detail.procurement_material.sub_order.uid',
        allow_null=True)
    location = serializers.CharField(source='warehouse.location', default='')

    class Meta:
        model = SteelMaterialInventoryDetail
        fields = ('id', 'material', 'batch_number', 'specification',
                  'entry_dt', 'material_number', 'work_order_uid',
                  'location', 'refund_times', 'count')


class AuxiliaryMaterialInventoryLedgerSerializer(serializers.ModelSerializer):
    specification = serializers.CharField(
        source='entry_detail.procurement_material.process_material.spec',
        allow_null=True, read_only=True)
    entry_dt = serializers.DateTimeField(
        source='entry_detail.entry.create_dt')
    factory = serializers.CharField(source='entry_detail.factory')
    # TODO: Replace with true field
    supplier = serializers.CharField(source='entry_detail.factory')
    entry_uid = serializers.CharField(source='entry_detail.entry.uid')
    entry_count = serializers.FloatField(source='entry_detail.count')

    class Meta:
        model = AuxiliaryMaterialInventoryDetail
        fields = ('id', 'specification', 'entry_count', 'entry_dt',
                  'entry_uid', 'factory', 'supplier', 'count')


class BoughtInComponentInventoryLedgerSerializer(serializers.ModelSerializer):
    material = serializers.CharField(
        source=('entry_detail.procurement_material'
                '.process_material.material.name'),
        allow_null=True, read_only=True)
    specification = serializers.CharField(
        source='entry_detail.procurement_material.process_material.spec',
        allow_null=True, read_only=True)
    entry_dt = serializers.DateTimeField(
        source='entry_detail.entry.create_dt')
    work_order_uid = serializers.CharField(
        source='entry_detail.procurement_material.sub_order.uid',
        allow_null=True)
    material_number = serializers.CharField(
        source=('entry_detail.procurement_material'
                '.process_material.material.uid'),
        allow_null=True, read_only=True)
    entry_uid = serializers.CharField(source='entry_detail.entry.uid')
    category = serializers.CharField(
        source='entry_detail.entry.get_category_display')

    class Meta:
        model = BoughtInComponentInventoryDetail
        fields = ('id', 'work_order_uid', 'specification', 'material',
                  'entry_dt', 'material_number', 'entry_uid', 'category',
                  'count')
