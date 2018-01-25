from rest_framework import serializers
from django.db import transaction

from Procurement.models import (Supplier, SupplierDocument, Quotation,
                                SupplyRelationship, SupplierCheck)
from Procurement.serializers import (BaseTransitionSerializer,
                                     BaseDynamicFieldSerializer)


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierDocumentSerializer(serializers.ModelSerializer):
    doc_name = serializers.SerializerMethodField(read_only=True)
    doc_size = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SupplierDocument
        fields = '__all__'

    def get_doc_name(self, obj):
        name = obj.path.name.split('/')
        return name[-1]

    def get_doc_size(self, obj):
        return obj.path.size


class QuotationSerializer(serializers.ModelSerializer):
    pretty_inventory_type = serializers.CharField(
            source='get_inventory_type_display')
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Quotation
        fields = '__all__'

    def get_price(self, obj):
        # TODO: 计算总价，较复杂
        return 0


class SupplierListSerializer(SupplierSerializer):
    docs = SupplierDocumentSerializer(read_only=True, many=True)

    class Meta(SupplierSerializer.Meta):
        fields = ('id', 'uid', 'name', 'docs')


class SupplierBiddingListSerializer(SupplierListSerializer):
    selected = serializers.SerializerMethodField(read_only=True)

    class Meta(SupplierListSerializer.Meta):
        fields = ('id', 'uid', 'name', 'docs', 'selected')

    def get_selected(self, obj):
        selected = False
        query = self.context['request'].query_params
        if query and 'id' in query and SupplyRelationship.objects.filter(
                supplier=obj, bidding_sheet_id=query['id']).count() > 0:
            selected = True
        return selected


class SupplierDetailSerializer(SupplierSerializer):
    docs = SupplierDocumentSerializer(read_only=True, many=True)
    quotations = QuotationSerializer(read_only=True, many=True)

    class Meta(SupplierSerializer.Meta):
        fields = ('id', 'uid', 'name', 'docs', 'quotations')


# 供应商关系
class BaseSupplyRelationshipSerializer(BaseDynamicFieldSerializer):

    class Meta:
        model = SupplyRelationship
        fields = ('id', 'bidding_sheet', 'supplier', 'A', 'B', 'C', 'D', 'E',
                  'F', 'G', 'scope', 'supplier_code', 'price', 'status',
                  'delivery_payment')


class SupplyRelationshipCreateSerializer(BaseSupplyRelationshipSerializer):
    suppliers = serializers.ListField(
        child=serializers.IntegerField(min_value=0,), write_only=True)

    class Meta(BaseSupplyRelationshipSerializer.Meta):
        fields = ('bidding_sheet', 'suppliers')

    def validate_suppliers(self, value):
        if len(value) != Supplier.objects.filter(
                id__in=value).count():
            raise serializers.ValidationError('列表中有未知标单ID')
        return value

    def create(self, validated_data):
        with transaction.atomic():
            suppliers = validated_data.pop('suppliers')
            sup_list = []
            for supplier in suppliers:
                sup_list.append(SupplyRelationship(
                    supplier_id=supplier, **validated_data))
            sup_object = SupplyRelationship.objects.bulk_create(sup_list)
            return sup_object[0]


# 供应商审核
class BaseSupplierCheckSerializer(BaseTransitionSerializer):

    class Meta:
        model = SupplierCheck
        fields = ('id', 'bidding_sheet', 'applicant', 'application_dt',
                  'project', 'estimated_price', 'basic_situation', 'status')
