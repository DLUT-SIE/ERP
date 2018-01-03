from django.db import transaction

from rest_framework import serializers

from Core.utils.fsm import TransitionSerializerMixin
from Core.utils.serializers import DynamicFieldSerializerMixin
from Procurement.models import ArrivalInspection, BiddingSheet
from Inventory.models import (
    WeldingMaterialEntry, SteelMaterialEntry, AuxiliaryMaterialEntry,
    BoughtInComponentEntry)
from .entry_detail import (
    WeldingMaterialEntryDetailSerializer,
    SteelMaterialEntryDetailSerializer,
    AuxiliaryMaterialEntryDetailSerializer,
    BoughtInComponentEntryDetailSerializer,
)


class AbstractEntryCreateSerializerMixin(serializers.Serializer):
    inspections = serializers.ListField(label='到货检验列表',
                                        child=serializers.IntegerField(),
                                        write_only=True)
    bidding_sheet = serializers.IntegerField(label='标单', write_only=True)

    class Meta:
        fields = ('inspections', 'bidding_sheet')

    def validate_inspections(self, inspection_ids):
        inspections = ArrivalInspection.objects.filter(id__in=inspection_ids)
        # TODO: Should we check the inspections are from the same biddingsheet?
        if not inspections:
            raise serializers.ValidationError('请至少选中一项')
        return inspections

    def validate_bidding_sheet(self, bidding_sheet_id):
        bidding_sheet = BiddingSheet.objects.filter(id=bidding_sheet_id)
        if not bidding_sheet:
            raise serializers.ValidationError('标单有误')
        return bidding_sheet[0]

    def create(self, validated_data):
        with transaction.atomic():
            self.Meta.model.create_entry(**validated_data)


class WeldingMaterialEntrySerializer(TransitionSerializerMixin,
                                     DynamicFieldSerializerMixin,
                                     serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    purchaser = serializers.CharField(source='purchaser.username',
                                      allow_null=True,
                                      read_only=True)
    inspector = serializers.CharField(source='inspector.username',
                                      allow_null=True,
                                      read_only=True)
    keeper = serializers.CharField(source='keeper.username',
                                   allow_null=True,
                                   read_only=True)
    details = WeldingMaterialEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = WeldingMaterialEntry
        fields = ('id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                  'purchaser', 'inspector', 'keeper', 'status',
                  'pretty_status', 'details', 'actions')
        read_only_fields = ('purchaser', 'inspector', 'keeper')


class WeldingMaterialEntryListSerializer(WeldingMaterialEntrySerializer):
    class Meta(WeldingMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'status', 'pretty_status')


class WeldingMaterialEntryCreateSerializer(AbstractEntryCreateSerializerMixin,
                                           serializers.ModelSerializer):
    class Meta(AbstractEntryCreateSerializerMixin.Meta):
        model = WeldingMaterialEntry


class SteelMaterialEntrySerializer(TransitionSerializerMixin,
                                   serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    purchaser = serializers.CharField(source='purchaser.username',
                                      allow_null=True,
                                      read_only=True)
    inspector = serializers.CharField(source='inspector.username',
                                      allow_null=True,
                                      read_only=True)
    keeper = serializers.CharField(source='keeper.username',
                                   allow_null=True,
                                   read_only=True)
    details = SteelMaterialEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = SteelMaterialEntry
        fields = ('id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                  'purchaser', 'inspector', 'keeper', 'status',
                  'pretty_status', 'details', 'actions')
        read_only_fields = ('purchaser', 'inspector', 'keeper')


class SteelMaterialEntryListSerializer(SteelMaterialEntrySerializer):
    pretty_steel_type = serializers.CharField(source='get_steel_type_display',
                                              read_only=True)

    class Meta(SteelMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'steel_type', 'pretty_steel_type', 'status',
                  'pretty_status')


class SteelMaterialEntryCreateSerializer(AbstractEntryCreateSerializerMixin,
                                         serializers.ModelSerializer):
    class Meta(AbstractEntryCreateSerializerMixin.Meta):
        model = SteelMaterialEntry


class AuxiliaryMaterialEntrySerializer(TransitionSerializerMixin,
                                       serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    purchaser = serializers.CharField(source='purchaser.username',
                                      allow_null=True,
                                      read_only=True)
    inspector = serializers.CharField(source='inspector.username',
                                      allow_null=True,
                                      read_only=True)
    keeper = serializers.CharField(source='keeper.username',
                                   allow_null=True,
                                   read_only=True)
    details = AuxiliaryMaterialEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = AuxiliaryMaterialEntry
        fields = ('id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                  'purchaser', 'inspector', 'keeper', 'status',
                  'pretty_status', 'details', 'actions')
        read_only_fields = ('purchaser', 'inspector', 'keeper')


class AuxiliaryMaterialEntryListSerializer(AuxiliaryMaterialEntrySerializer):
    class Meta(AuxiliaryMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'status', 'pretty_status')


class AuxiliaryMaterialEntryCreateSerializer(
        AbstractEntryCreateSerializerMixin, serializers.ModelSerializer):
    class Meta(AbstractEntryCreateSerializerMixin.Meta):
        model = AuxiliaryMaterialEntry


class BoughtInComponentEntrySerializer(TransitionSerializerMixin,
                                       serializers.ModelSerializer):
    pretty_category = serializers.CharField(source='get_category_display',
                                            read_only=True)
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    purchaser = serializers.CharField(source='purchaser.username',
                                      allow_null=True, read_only=True)
    inspector = serializers.CharField(source='inspector.username',
                                      allow_null=True, read_only=True)
    details = BoughtInComponentEntryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = BoughtInComponentEntry
        fields = ('id', 'uid', 'bidding_sheet', 'source', 'create_dt',
                  'source', 'category', 'pretty_category', 'purchaser',
                  'inspector', 'keeper', 'status', 'pretty_status',
                  'details', 'actions')
        read_only_fields = ('purchaser', 'inspector', 'keeper')


class BoughtInComponentEntryListSerializer(BoughtInComponentEntrySerializer):
    class Meta(BoughtInComponentEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'source', 'pretty_category',
                  'purchaser', 'status', 'pretty_status')


class BoughtInComponentEntryCreateSerializer(
        AbstractEntryCreateSerializerMixin, serializers.ModelSerializer):
    class Meta(AbstractEntryCreateSerializerMixin.Meta):
        model = BoughtInComponentEntry
