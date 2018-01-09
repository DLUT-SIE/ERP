from rest_framework import serializers
from Procurement.models import PurchaseOrder, ProcurementMaterial
from Process.serializers import ProcessMaterialSerializer
from Procurement.serializers import (BaseTransitionSerializer,
                                     BaseDynamicFieldSerializer)


# 采购物料
class BaseProcurementMaterialSerializer(BaseDynamicFieldSerializer):

    class Meta:
        model = ProcurementMaterial
        fields = (
            'id', 'process_material', 'merged_material', 'purchase_order',
            'sub_order', 'inventory_type', 'batch_number', 'material_number',
            'delivery_dt', 'category', 'finished', 'add_to_detail', 'count',
            'weight')


# Read & Update
class ProcurementMaterialReadSerializer(BaseProcurementMaterialSerializer):

    process_material = ProcessMaterialSerializer(
        required=False, allow_null=True, read_only=True)

    class Meta(BaseProcurementMaterialSerializer.Meta):
        fields = (
            'id', 'process_material', 'merged_material', 'purchase_order',
            'sub_order', 'inventory_type', 'batch_number', 'material_number',
            'delivery_dt', 'category', 'finished', 'add_to_detail', 'count',
            'weight')


class ProcurementMaterialListSerializer(BaseProcurementMaterialSerializer):

    process_material = ProcessMaterialSerializer(
        required=False, allow_null=True, read_only=True)

    total_weight = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseProcurementMaterialSerializer.Meta):
        fields = (
            'id', 'process_material', 'merged_material', 'purchase_order',
            'sub_order', 'inventory_type', 'batch_number', 'material_number',
            'delivery_dt', 'category', 'finished', 'add_to_detail', 'count',
            'weight', 'total_weight')

    def get_total_weight(self, obj):
        return obj.count * obj.weight


# 采购单
class BasePurchaseOrderSerializer(BaseTransitionSerializer):

    work_order_uid = serializers.CharField(source='work_order.uid',
                                           read_only=True)
    create_dt = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ('id', 'uid', 'work_order', 'create_dt', 'status', 'lister',
                  'list_dt', 'chief', 'audit_dt', 'approver', 'approve_dt',
                  'tech_requirement', 'category', 'revised_number',
                  'work_order_uid')


# 嵌套写
class PurchaseOrderCreateSerializer(BasePurchaseOrderSerializer):

    class Meta(BasePurchaseOrderSerializer.Meta):
        read_only_fields = ('id', 'create_dt', 'lister', 'list_dt',
                            'chief', 'audit_dt', 'approver', 'approve_dt',
                            'tech_requirement', 'revised_number',
                            'work_order_uid')


# Read &  Update
class PurchaseOrderReadSerializer(BasePurchaseOrderSerializer):

    status_name = serializers.CharField(source='get_status_display',
                                        read_only=True)

    class Meta(BasePurchaseOrderSerializer.Meta):
        fields = ('id', 'uid', 'work_order', 'create_dt', 'status', 'lister',
                  'list_dt', 'chief', 'audit_dt', 'approver', 'approve_dt',
                  'tech_requirement', 'category', 'revised_number',
                  'work_order_uid', 'status_name')


# List
class PurchaseOrderListSerializer(BasePurchaseOrderSerializer):

    class Meta(BasePurchaseOrderSerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'status', 'category',
                  'revised_number')
