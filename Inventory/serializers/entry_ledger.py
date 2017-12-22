from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialEntryDetail, SteelMaterialEntryDetail,
    AuxiliaryMaterialEntryDetail, BoughtInComponentEntryDetail)


class WeldingMaterialEntryLedgerSerializer(serializers.ModelSerializer):
    material_mark = serializers.CharField(
        source='procurement_material.process_material.name')
    specification = serializers.CharField(
        source='procurement_material.process_material.spec')
    entry_dt = serializers.DateTimeField(source='entry.create_dt')
    material_number = serializers.CharField(
        source='procurement_material.process_material.material.uid')

    class Meta:
        model = WeldingMaterialEntryDetail
        fields = ('id', 'material_mark', 'specification', 'entry_dt',
                  'material_number', 'factory', 'count', 'weight')
        read_only_fields = ('material_mark', 'specification', 'entry_dt',
                            'material_number', 'factory', 'count', 'weight')


class SteelMaterialEntryLedgerSerializer(serializers.ModelSerializer):
    material = serializers.CharField(
        source='procurement_material.process_material.material.name')
    specification = serializers.CharField(
        source='procurement_material.process_material.spec')
    entry_dt = serializers.DateTimeField(source='entry.create_dt')
    material_number = serializers.CharField(
        source='procurement_material.process_material.material.uid')
    work_order_uid = serializers.CharField(
        source=('entry.bidding_sheet.purchase_order.work_order.uid'))

    class Meta:
        model = SteelMaterialEntryDetail
        fields = ('id', 'material', 'specification', 'entry_dt',
                  'material_number', 'work_order_uid', 'count', 'weight')
        read_only_fields = ('material', 'specification', 'entry_dt',
                            'material_number', 'work_order_uid', 'count',
                            'weight')


class AuxiliaryMaterialEntryLedgerSerializer(serializers.ModelSerializer):
    specification = serializers.CharField(
        source='procurement_material.process_material.spec')
    entry_dt = serializers.DateTimeField(source='entry.create_dt')
    # TODO: Replace with true field
    supplier = serializers.CharField(source='factory')
    entry_uid = serializers.CharField(source='entry.uid')

    class Meta:
        model = AuxiliaryMaterialEntryDetail
        fields = ('id', 'specification', 'entry_dt', 'entry_uid', 'factory',
                  'supplier', 'count')
        read_only_fields = ('specification', 'entry_dt', 'entry_uid',
                            'factory', 'supplier', 'count')


class BoughtInComponentEntryLedgerSerializer(serializers.ModelSerializer):
    material = serializers.CharField(
        source='procurement_material.process_material.material.name')
    specification = serializers.CharField(
        source='procurement_material.process_material.spec')
    entry_dt = serializers.DateTimeField(source='entry.create_dt')
    work_order_uid = serializers.CharField(
        source=('entry.bidding_sheet.purchase_order.work_order.uid'))
    material_number = serializers.CharField(
        source='procurement_material.process_material.material.uid')
    entry_uid = serializers.CharField(source='entry.uid')

    class Meta:
        model = BoughtInComponentEntryDetail
        fields = ('id', 'work_order_uid', 'specification', 'material',
                  'entry_dt', 'material_number', 'entry_uid', 'count')
        read_only_fields = ('work_order_uid', 'specification', 'material',
                            'entry_dt', 'material_number', 'entry_uid',
                            'count')