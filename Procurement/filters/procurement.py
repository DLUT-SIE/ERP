from django_filters import rest_framework as filters

from Procurement.models import (PurchaseOrder, ProcurementMaterial)
from Procurement import PURCHASE_ORDER_STATUS_CHOICES
from Process.models import (ProcessMaterial)
from Procurement import (PROCUREMENT_MATERIAL_STATUS, INVENTORY_TYPE)


class PurchaseOrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(name='status', lookup_expr='exact',
                                  choices=PURCHASE_ORDER_STATUS_CHOICES)
    uid = filters.CharFilter(name='uid', lookup_expr='icontains')

    category = filters.CharFilter(name='category', lookup_expr='exact')

    class Meta:
        model = PurchaseOrder
        fields = ('status', 'uid', 'category')


class ProcurementMaterialFilter(filters.FilterSet):
    purchase_order_uid = filters.CharFilter(method='filter_purchase_order')

    process_material_name = filters.CharFilter(
        method='filter_process_material_name')

    sub_work_order_uid = filters.CharFilter(method='filter_sub_work_order_uid')

    status = filters.MultipleChoiceFilter(name='status',
                                          choices=PROCUREMENT_MATERIAL_STATUS)

    finished = filters.BooleanFilter(name='finished', lookup_expr='exact')

    purchase_order = filters.CharFilter(name='purchase_order',
                                        lookup_expr='exact')
   
    inventory_type = filters.ChoiceFilter(name='inventory_type',
                                          choices=INVENTORY_TYPE)

    class Meta:
        model = ProcurementMaterial
        fields = ('purchase_order_uid', 'process_material_name',
                  'sub_work_order_uid', 'purchase_order', 'status', 'finished',
                  'inventory_type')

    def filter_purchase_order(self, query_set, name, value):
        purchase_order = PurchaseOrder.objects.filter(uid=value)
        if not purchase_order:
            return self.Meta.model.objects.none()
        procurement_materials = self.Meta.model.objects.filter(
            purchase_order=purchase_order[0])
        return procurement_materials

    # 根据工艺物料的名称 模糊查询采购物料
    def filter_process_material_name(self, query_set, name, value):
        process_materials = ProcessMaterial.objects.filter(
            name__contains=value)
        if not process_materials:
            return self.Meta.model.objects.none()
        procurement_materials = self.Meta.model.objects.filter(
            process_material__in=process_materials)
        return procurement_materials

    def filter_sub_work_order_uid(self, query_set, name, value):
        value = value.split('-') #参见SubWorkOrder模型定义
        if not value or len(value) != 2 or '' in value:
            return self.Meta.model.objects.none()
        procurement_materials = self.Meta.model.objects.filter(
            sub_order__work_order__uid=value[0], sub_order__index=value[1])
        if not procurement_materials:
            return self.Meta.model.objects.none()
        return procurement_materials
