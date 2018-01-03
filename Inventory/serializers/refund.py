from django.db import transaction

from rest_framework import serializers

from Core.utils.fsm import TransitionSerializerMixin
from Inventory import APPLYCARD_STATUS_END
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


class AbstractRefundCardCreateSerializerMixin(serializers.Serializer):
    apply_card = serializers.IntegerField(label='领用卡', write_only=True)
    details_dict = serializers.DictField(label='领用明细',
                                         child=serializers.IntegerField(),
                                         write_only=True)

    class Meta:
        model = None
        fields = ('apply_card', 'details_dict')

    def validate_details_dict(self, details_dict):
        """
        将 {'apply_detail_id': count} 转化为 [(apply_detail, count)]
        """
        details = []
        ids = [int(id) for id in details_dict.keys()]
        apply_cls = self.Meta.model.apply_cls
        apply_detail_cls = apply_cls.apply_detail_cls or apply_cls
        apply_details = apply_detail_cls.objects.filter(id__in=ids)
        if apply_details.count() != len(details_dict):
            raise serializers.ValidationError('领用明细有误')
        details = {detail: details_dict[str(detail.id)]
                   for detail in apply_details}
        return details

    def validate_apply_card(self, apply_card_id):
        apply_card = self.Meta.model.apply_cls.objects.filter(id=apply_card_id)
        if not apply_card:
            raise serializers.ValidationError('不存在该领用卡')
        apply_card = apply_card[0]
        if apply_card.status != APPLYCARD_STATUS_END:
            raise serializers.ValidationError('领用卡状态不符合退库要求')
        return apply_card

    def validate(self, attrs):
        # TODO: 领用明细应与领用卡关联
        print('validate', attrs)
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            self.Meta.model.create_refund_cards(**validated_data)


class WeldingMaterialRefundCardSerializer(TransitionSerializerMixin,
                                          serializers.ModelSerializer):
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
                  'status', 'pretty_status', 'actions')
        read_only_fields = ('refunder', 'keeper')


class WeldingMaterialRefundCardListSerializer(
        WeldingMaterialRefundCardSerializer):
    welding_seam_uid = serializers.CharField(default='', read_only=True)

    class Meta(WeldingMaterialRefundCardSerializer.Meta):
        fields = ('id', 'sub_order_uid', 'department', 'create_dt', 'uid',
                  'welding_seam_uid', 'status', 'pretty_status')


class WeldingMaterialRefundCardCreateSerializer(
        AbstractRefundCardCreateSerializerMixin,
        serializers.ModelSerializer):
    class Meta(AbstractRefundCardCreateSerializerMixin.Meta):
        model = WeldingMaterialRefundCard


class SteelMaterialRefundCardSerializer(TransitionSerializerMixin,
                                        serializers.ModelSerializer):
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
                  'board_details', 'bar_details', 'actions')
        read_only_fields = ('refunder', 'inspector', 'keeper')


class SteelMaterialRefundCardListSerializer(
        SteelMaterialRefundCardSerializer):
    class Meta(SteelMaterialRefundCardSerializer.Meta):
        fields = ('id', 'create_dt', 'uid', 'sub_order_uid', 'steel_type',
                  'refunder', 'status', 'pretty_status')


class SteelMaterialRefundCardCreateSerializer(
        AbstractRefundCardCreateSerializerMixin,
        serializers.ModelSerializer):
    class Meta(AbstractRefundCardCreateSerializerMixin.Meta):
        model = SteelMaterialRefundCard


class BoughtInComponentRefundCardSerializer(TransitionSerializerMixin,
                                            serializers.ModelSerializer):
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
                  'keeper', 'status', 'pretty_status', 'details', 'actions')
        read_only_fields = ('refunder', 'keeper')


class BoughtInComponentRefundCardListSerializer(
        BoughtInComponentRefundCardSerializer):
    class Meta(BoughtInComponentRefundCardSerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'refunder', 'status',
                  'pretty_status')


class BoughtInComponentRefundCardCreateSerializer(
        AbstractRefundCardCreateSerializerMixin,
        serializers.ModelSerializer):
    class Meta(AbstractRefundCardCreateSerializerMixin.Meta):
        model = BoughtInComponentRefundCard
