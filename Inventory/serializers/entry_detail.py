from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialEntryDetail, SteelMaterialEntryDetail,
    AuxiliaryMaterialEntryDetail, BoughtInComponentEntryDetail)


class WeldingMaterialEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldingMaterialEntryDetail
        fields = '__all__'


class SteelMaterialEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteelMaterialEntryDetail
        fields = '__all__'


class AuxiliaryMaterialEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuxiliaryMaterialEntryDetail
        fields = '__all__'


class BoughtInComponentEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoughtInComponentEntryDetail
        fields = '__all__'
