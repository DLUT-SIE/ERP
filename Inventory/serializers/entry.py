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
    purchaser = serializers.CharField(source='purchaser.username',
                                      allow_null=True, default=None)
    inspector = serializers.CharField(source='inspector.username',
                                      allow_null=True, default=None)
    keeper = serializers.CharField(source='keeper.username',
                                   allow_null=True, default=None)
    details = WeldingMaterialEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = WeldingMaterialEntry
        fields = ('id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                  'purchaser', 'inspector', 'keeper', 'status',
                  'pretty_status', 'details')


class WeldingMaterialEntryListSerializer(WeldingMaterialEntrySerializer):
    class Meta(WeldingMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'status', 'pretty_status')


class SteelMaterialEntrySerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    purchaser = serializers.CharField(source='purchaser.username',
                                      allow_null=True, default=None)
    inspector = serializers.CharField(source='inspector.username',
                                      allow_null=True, default=None)
    keeper = serializers.CharField(source='keeper.username',
                                   allow_null=True, default=None)
    details = SteelMaterialEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = SteelMaterialEntry
        fields = ('id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                  'purchaser', 'inspector', 'keeper', 'status',
                  'pretty_status', 'details')


class SteelMaterialEntryListSerializer(SteelMaterialEntrySerializer):
    pretty_steel_type = serializers.CharField(source='get_steel_type_display',
                                              read_only=True)

    class Meta(SteelMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'steel_type', 'pretty_steel_type', 'status',
                  'pretty_status')


class AuxiliaryMaterialEntrySerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    purchaser = serializers.CharField(source='purchaser.username',
                                      allow_null=True, default=None)
    inspector = serializers.CharField(source='inspector.username',
                                      allow_null=True, default=None)
    keeper = serializers.CharField(source='keeper.username',
                                   allow_null=True, default=None)
    details = AuxiliaryMaterialEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = AuxiliaryMaterialEntry
        fields = ('id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                  'purchaser', 'inspector', 'keeper', 'status',
                  'pretty_status', 'details')


class AuxiliaryMaterialEntryListSerializer(AuxiliaryMaterialEntrySerializer):
    class Meta(AuxiliaryMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'status', 'pretty_status')


class BoughtInComponentEntrySerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    purchaser = serializers.CharField(source='purchaser.username',
                                      allow_null=True, default=None)
    inspector = serializers.CharField(source='inspector.username',
                                      allow_null=True, default=None)
    details = BoughtInComponentEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = BoughtInComponentEntry
        fields = ('id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                  'purchaser', 'inspector', 'keeper', 'status',
                  'pretty_status', 'details')


class BoughtInComponentEntryListSerializer(BoughtInComponentEntrySerializer):
    class Meta(BoughtInComponentEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'status', 'pretty_status')
