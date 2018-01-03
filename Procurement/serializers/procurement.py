from rest_framework import serializers

from Procurement.models import PurchaseOrder, ProcurementMaterial
from Process.serializers import ProcessMaterialSerializer


# 采购物料
class BaseProcurementMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcurementMaterial
        fields = (
            'id', 'process_material', 'merged_material', 'purchase_order',
            'sub_order', 'inventory_type', 'batch_number', 'material_number',
            'delivery_dt', 'category', 'finished', 'add_to_detail')


# Read & Update
class ProcurementMaterialReadSerializer(BaseProcurementMaterialSerializer):

    process_material = ProcessMaterialSerializer(
        required=False, allow_null=True, read_only=True)

    class Meta(BaseProcurementMaterialSerializer.Meta):
        fields = (
            'id', 'process_material', 'merged_material', 'purchase_order',
            'sub_order', 'inventory_type', 'batch_number', 'material_number',
            'delivery_dt', 'category', 'finished', 'add_to_detail')


class ProcurementMaterialListSerializer(BaseProcurementMaterialSerializer):

    class Meta(BaseProcurementMaterialSerializer.Meta):
        fields = ('id', 'material_number', 'purchase_order', 'category',
                  'finished', 'add_to_detail')


# 采购单
class BasePurchaseOrderSerializer(serializers.ModelSerializer):

    work_order_uid = serializers.CharField(source='work_order.uid',
                                           read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ('id', 'uid', 'work_order', 'create_dt', 'status', 'lister',
                  'list_dt', 'chief', 'audit_dt', 'approver', 'approve_dt',
                  'tech_requirement', 'category', 'revised_number',
                  'work_order_uid')


# 嵌套写
class PurchaseOrderCreateSerializer(BasePurchaseOrderSerializer):

    class Meta(BasePurchaseOrderSerializer.Meta):
        read_only_fields = ('id', 'create_dt', 'status', 'lister', 'list_dt',
                            'chief', 'audit_dt', 'approver', 'approve_dt',
                            'tech_requirement', 'revised_number',
                            'work_order_uid')


# Read &  Update
class PurchaseOrderReadSerializer(BasePurchaseOrderSerializer):

    procurementmaterial_set = ProcurementMaterialReadSerializer(
        read_only=True, many=True, required=False)

    class Meta(BasePurchaseOrderSerializer.Meta):
        fields = ('id', 'uid', 'work_order', 'create_dt', 'status', 'lister',
                  'list_dt', 'chief', 'audit_dt', 'approver', 'approve_dt',
                  'tech_requirement', 'category', 'revised_number',
                  'work_order_uid', 'procurementmaterial_set')


# List
class PurchaseOrderListSerializer(BasePurchaseOrderSerializer):

    class Meta(BasePurchaseOrderSerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'status', 'category',
                  'revised_number', )
