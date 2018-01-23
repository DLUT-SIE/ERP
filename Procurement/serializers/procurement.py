from rest_framework import serializers
from Procurement.models import PurchaseOrder, ProcurementMaterial
from Process.serializers import ProcessMaterialSerializer
from Procurement.serializers import (BaseTransitionSerializer,
                                     BaseDynamicFieldSerializer)


# 采购物料
class BaseProcurementMaterialSerializer(BaseDynamicFieldSerializer):

    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)

    class Meta:
        model = ProcurementMaterial
        fields = (
            'id', 'process_material', 'merged_material', 'purchase_order',
            'sub_order', 'inventory_type', 'batch_number', 'material_number',
            'delivery_dt', 'category', 'finished', 'status', 'count',
            'weight', 'pretty_status')


# Read & Update
class ProcurementMaterialReadSerializer(BaseProcurementMaterialSerializer):

    process_material = ProcessMaterialSerializer(
        required=False, allow_null=True, read_only=True)

    class Meta(BaseProcurementMaterialSerializer.Meta):
        fields = (
            'id', 'process_material', 'merged_material', 'purchase_order',
            'sub_order', 'inventory_type', 'batch_number', 'material_number',
            'delivery_dt', 'category', 'finished', 'status', 'count',
            'weight', 'pretty_status')
        read_only_fields = ('material_number', 'category')


class ProcurementMaterialListSerializer(BaseProcurementMaterialSerializer):

    process_material = ProcessMaterialSerializer(
        required=False, allow_null=True, read_only=True)

    total_weight = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseProcurementMaterialSerializer.Meta):
        fields = (
            'id', 'process_material', 'merged_material', 'purchase_order',
            'sub_order', 'inventory_type', 'batch_number', 'material_number',
            'delivery_dt', 'category', 'finished', 'status', 'count',
            'weight', 'total_weight', 'pretty_status')

    def get_total_weight(self, obj):
        return obj.count * obj.weight


# 采购单
class BasePurchaseOrderSerializer(BaseTransitionSerializer):

    create_dt = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ('id', 'uid', 'create_dt', 'status', 'lister',
                  'list_dt', 'chief', 'audit_dt', 'approver', 'approve_dt',
                  'tech_requirement', 'category', 'revised_number')


# 嵌套写
class PurchaseOrderCreateSerializer(BasePurchaseOrderSerializer):

    class Meta(BasePurchaseOrderSerializer.Meta):
        read_only_fields = ('id', 'create_dt', 'lister', 'list_dt',
                            'chief', 'audit_dt', 'approver', 'approve_dt',
                            'tech_requirement', 'category', 'revised_number',
                            'status')


# Read &  Update
class PurchaseOrderReadSerializer(BasePurchaseOrderSerializer):

    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)

    class Meta(BasePurchaseOrderSerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'status', 'lister', 'list_dt',
                  'chief', 'audit_dt', 'approver', 'approve_dt',
                  'tech_requirement', 'category', 'revised_number',
                  'pretty_status')


# List
class PurchaseOrderListSerializer(BasePurchaseOrderSerializer):

    class Meta(BasePurchaseOrderSerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'status', 'category',
                  'revised_number')
