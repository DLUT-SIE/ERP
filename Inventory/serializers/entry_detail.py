from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialEntryDetail, SteelMaterialEntryDetail,
    AuxiliaryMaterialEntryDetail, BoughtInComponentEntryDetail)


class WeldingMaterialEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldingMaterialEntryDetail
        fields = ('id', 'entry', 'procurement_material', 'weight', 'count',
                  'unit', 'factory', 'remark', 'production_dt')


class SteelMaterialEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteelMaterialEntryDetail
        fields = ('id', 'entry', 'procurement_material', 'weight', 'count',
                  'unit', 'factory', 'remark', 'length')


class AuxiliaryMaterialEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuxiliaryMaterialEntryDetail
        fields = ('id', 'entry', 'procurement_material', 'weight', 'count',
                  'unit', 'factory', 'remark')


class BoughtInComponentEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoughtInComponentEntryDetail
        fields = ('id', 'entry', 'procurement_material', 'weight', 'count',
                  'unit', 'factory', 'remark')
