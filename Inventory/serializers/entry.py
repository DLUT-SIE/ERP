from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialEntry, SteelMaterialEntry, AuxiliaryMaterialEntry,
    BoughtInComponentEntry)

from .entry_detail import (
    WeldingMaterialEntryDetailSerializer,
    SteelMaterialEntryDetailSerializer,
    AuxiliaryMaterialEntryDetailSerializer,
    BoughtInComponentEntryDetailSerializer,
)


class WeldingMaterialEntrySerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    purchaser = serializers.CharField(source='purchaser.username')
    inspector = serializers.CharField(source='inspector.username')
    keeper = serializers.CharField(source='keeper.username',
                                   allow_null=True, default=None)
    details = WeldingMaterialEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = WeldingMaterialEntry
        fields = '__all__'


class WeldingMaterialEntryListSerializer(WeldingMaterialEntrySerializer):
    class Meta(WeldingMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'status', 'pretty_status')


class SteelMaterialEntrySerializer(serializers.ModelSerializer):
    pretty_steel_type = serializers.CharField(source='get_steel_type_display',
                                              read_only=True)
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    details = SteelMaterialEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = SteelMaterialEntry
        fields = '__all__'


class SteelMaterialEntryListSerializer(SteelMaterialEntrySerializer):
    class Meta(SteelMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'steel_type', 'pretty_steel_type', 'status',
                  'pretty_status')


class AuxiliaryMaterialEntrySerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    details = AuxiliaryMaterialEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = AuxiliaryMaterialEntry
        fields = '__all__'


class AuxiliaryMaterialEntryListSerializer(AuxiliaryMaterialEntrySerializer):
    class Meta(AuxiliaryMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'status', 'pretty_status')


class BoughtInComponentEntrySerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    details = BoughtInComponentEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = BoughtInComponentEntry
        fields = '__all__'


class BoughtInComponentEntryListSerializer(BoughtInComponentEntrySerializer):
    class Meta(BoughtInComponentEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'status', 'pretty_status')
