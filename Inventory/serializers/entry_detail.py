from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialEntryDetail, SteelMaterialEntryDetail,
    AuxiliaryMaterialEntryDetail, BoughtInComponentEntryDetail)


class WeldingMaterialEntryDetailSerializer(serializers.ModelSerializer):
    batch_number = serializers.CharField(
        source='procurement_material.batch_number', read_only=True,
        allow_null=True)
    material_number = serializers.CharField(
        source='procurement_material.material_number', read_only=True,
        allow_null=True)

    class Meta:
        model = WeldingMaterialEntryDetail
        fields = ('id', 'entry', 'procurement_material', 'weight', 'count',
                  'unit', 'factory', 'remark', 'production_dt',
                  'batch_number', 'material_number')


class SteelMaterialEntryDetailSerializer(serializers.ModelSerializer):
    batch_number = serializers.CharField(
        source='procurement_material.batch_number', read_only=True,
        allow_null=True)

    class Meta:
        model = SteelMaterialEntryDetail
        fields = ('id', 'entry', 'procurement_material', 'weight', 'count',
                  'unit', 'factory', 'remark', 'length',
                  'batch_number')


class AuxiliaryMaterialEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuxiliaryMaterialEntryDetail
        fields = ('id', 'entry', 'procurement_material', 'weight', 'count',
                  'unit', 'factory', 'remark')


class BoughtInComponentEntryDetailSerializer(serializers.ModelSerializer):
    batch_number = serializers.CharField(
        source='procurement_material.batch_number', read_only=True,
        allow_null=True)

    class Meta:
        model = BoughtInComponentEntryDetail
        fields = ('id', 'entry', 'procurement_material', 'weight', 'count',
                  'unit', 'factory', 'remark', 'batch_number')
