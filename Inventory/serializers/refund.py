from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialRefundCard,
    SteelMaterialRefundCard,
    BoughtInComponentRefundCard,
)
from .refund_detail import (
    BoardSteelMaterialRefundDetailSerializer,
    BarSteelMaterialRefundDetailSerializer,
    BoughtInComponentRefundDetailSerializer,
)


class WeldingMaterialRefundCardSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='apply_card.department',
                                       read_only=True)
    sub_order_uid = serializers.CharField(source='apply_card.sub_order.uid',
                                          read_only=True)
    apply_card_create_dt = serializers.CharField(source='apply_card.create_dt',
                                                 read_only=True)
    apply_card_uid = serializers.CharField(source='apply_card.uid',
                                           read_only=True)
    model = serializers.CharField(default='', read_only=True)
    specification = serializers.CharField(
        source='apply_card.process_material.spec', read_only=True)
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)

    class Meta:
        model = WeldingMaterialRefundCard
        fields = ('id', 'department', 'create_dt', 'uid', 'sub_order_uid',
                  'apply_card_create_dt', 'apply_card_uid', 'model',
                  'specification', 'weight', 'count', 'refunder', 'keeper',
                  'status', 'pretty_status')


class WeldingMaterialRefundCardListSerializer(
        WeldingMaterialRefundCardSerializer):
    welding_seam_uid = serializers.CharField(default='', read_only=True)

    class Meta(WeldingMaterialRefundCardSerializer.Meta):
        fields = ('id', 'sub_order_uid', 'department', 'create_dt', 'uid',
                  'welding_seam_uid', 'status', 'pretty_status')


class SteelMaterialRefundCardSerializer(serializers.ModelSerializer):
    sub_order_uid = serializers.CharField(source='apply_card.sub_order.uid',
                                          read_only=True)
    steel_type = serializers.CharField(default='', read_only=True)
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    board_details = BoardSteelMaterialRefundDetailSerializer(many=True,
                                                             read_only=True)
    bar_details = BarSteelMaterialRefundDetailSerializer(many=True,
                                                         read_only=True)

    class Meta:
        model = SteelMaterialRefundCard
        fields = ('id', 'sub_order_uid', 'create_dt', 'uid', 'steel_type',
                  'refunder', 'inspector', 'keeper', 'status', 'pretty_status',
                  'board_details', 'bar_details')


class SteelMaterialRefundCardListSerializer(
        SteelMaterialRefundCardSerializer):
    class Meta(SteelMaterialRefundCardSerializer.Meta):
        fields = ('id', 'create_dt', 'uid', 'sub_order_uid', 'steel_type',
                  'refunder', 'status', 'pretty_status')


class BoughtInComponentRefundCardSerializer(serializers.ModelSerializer):
    sub_order_uid = serializers.CharField(source='apply_card.sub_order.uid',
                                          read_only=True)
    department = serializers.CharField(source='apply_card.department',
                                       read_only=True)
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    details = BoughtInComponentRefundDetailSerializer(many=True,
                                                      read_only=True)

    class Meta:
        model = BoughtInComponentRefundCard
        fields = ('id', 'sub_order_uid', 'department', 'uid', 'refunder',
                  'keeper', 'status', 'pretty_status', 'details')


class BoughtInComponentRefundCardListSerializer(
        BoughtInComponentRefundCardSerializer):
    class Meta(BoughtInComponentRefundCardSerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'refunder', 'status',
                  'pretty_status')
