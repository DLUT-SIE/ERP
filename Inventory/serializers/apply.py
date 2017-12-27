from rest_framework import serializers

from Core.utils.fsm import TransitionSerializerMixin
from Inventory.models import (
    WeldingMaterialApplyCard,
    SteelMaterialApplyCard,
    AuxiliaryMaterialApplyCard,
    BoughtInComponentApplyCard,
)
from .apply_detail import (
    SteelMaterialApplyDetailSerializer,
    BoughtInComponentApplyDetailSerializer,
)


class WeldingMaterialApplyCardSerializer(TransitionSerializerMixin,
                                         serializers.ModelSerializer):
    sub_order_uid = serializers.CharField(source='sub_order.uid',
                                          read_only=True)
    welding_seam_uid = serializers.CharField(default='', read_only=True)
    material_mark = serializers.CharField(
        source='process_material.name', read_only=True)
    material_code = serializers.CharField(
        source='material_number', read_only=True)
    model = serializers.CharField(default='', read_only=True)
    specification = serializers.CharField(source='process_material.spec',
                                          read_only=True)
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)

    class Meta:
        model = WeldingMaterialApplyCard
        fields = ('id', 'department', 'create_dt', 'uid', 'sub_order_uid',
                  'welding_seam_uid', 'material_mark', 'model',
                  'specification', 'apply_weight', 'apply_count',
                  'material_code', 'actual_weight', 'actual_count',
                  'applicant', 'auditor', 'inspector', 'keeper',
                  'status', 'pretty_status', 'actions')
        read_only_fields = ('applicant', 'auditor', 'inspector', 'keeper')


class WeldingMaterialApplyCardListSerializer(
        WeldingMaterialApplyCardSerializer):
    class Meta(WeldingMaterialApplyCardSerializer.Meta):
        fields = ('id', 'sub_order_uid', 'welding_seam_uid', 'material_mark',
                  'model', 'specification', 'department', 'create_dt',
                  'uid', 'status', 'pretty_status')


class SteelMaterialApplyCardSerializer(TransitionSerializerMixin,
                                       serializers.ModelSerializer):
    details = SteelMaterialApplyDetailSerializer(many=True, read_only=True)

    class Meta:
        model = SteelMaterialApplyCard
        fields = ('id', 'department', 'create_dt', 'uid', 'applicant',
                  'auditor', 'inspector', 'keeper', 'details', 'status',
                  'actions')
        read_only_fields = ('applicant', 'auditor', 'inspector', 'keeper')


class SteelMaterialApplyCardListSerializer(SteelMaterialApplyCardSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)

    class Meta(SteelMaterialApplyCardSerializer.Meta):
        fields = ('id', 'create_dt', 'uid', 'applicant', 'department',
                  'status', 'pretty_status')


class AuxiliaryMaterialApplyCardSerializer(TransitionSerializerMixin,
                                           serializers.ModelSerializer):
    sub_order_uid = serializers.CharField(source='sub_order.uid',
                                          read_only=True, default='')
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    apply_inventory_name = serializers.CharField(
        source='apply_inventory.entry_detail.procurement_material',
        read_only=True)
    actual_inventory_name = serializers.CharField(
        source='actual_inventory.entry_detail.procurement_material',
        read_only=True, allow_null=True)

    class Meta:
        model = AuxiliaryMaterialApplyCard
        fields = ('id', 'sub_order_uid', 'department', 'uid', 'create_dt',
                  'applicant', 'auditor', 'inspector', 'keeper',
                  'status', 'pretty_status', 'apply_inventory',
                  'apply_inventory_name', 'apply_count',
                  'actual_inventory_name', 'actual_inventory',
                  'actual_count', 'remark', 'actions')
        read_only_fields = ('applicant', 'auditor', 'inspector', 'keeper')


class AuxiliaryMaterialApplyCardListSerializer(
        AuxiliaryMaterialApplyCardSerializer):
    class Meta(AuxiliaryMaterialApplyCardSerializer.Meta):
        fields = ('id', 'sub_order_uid', 'uid', 'create_dt',
                  'apply_inventory_name', 'apply_count', 'applicant',
                  'department', 'status', 'pretty_status')


class BoughtInComponentApplyCardSerializer(TransitionSerializerMixin,
                                           serializers.ModelSerializer):
    sub_order_uid = serializers.CharField(source='sub_order.uid',
                                          read_only=True, default='')
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    details = BoughtInComponentApplyDetailSerializer(many=True, read_only=True)

    class Meta:
        model = BoughtInComponentApplyCard
        fields = ('id', 'revised_number', 'sample_report', 'sub_order_uid',
                  'department', 'create_dt', 'uid', 'applicant', 'auditor',
                  'inspector', 'keeper', 'status', 'pretty_status', 'details',
                  'actions')
        read_only_fields = ('applicant', 'auditor', 'inspector', 'keeper')


class BoughtInComponentApplyCardListSerializer(
        BoughtInComponentApplyCardSerializer):
    class Meta(BoughtInComponentApplyCardSerializer.Meta):
        fields = ('id', 'sub_order_uid', 'uid', 'create_dt', 'applicant',
                  'department', 'status', 'pretty_status')
