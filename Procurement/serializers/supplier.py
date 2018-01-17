from rest_framework import serializers

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

    class Meta:
        model = Quotation
        fields = '__all__'


class SupplierListSerializer(SupplierSerializer):
    docs = SupplierDocumentSerializer(read_only=True, many=True)

    class Meta(SupplierSerializer.Meta):
        fields = ('id', 'uid', 'name', 'docs')


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


# 供应商审核
class BaseSupplierCheckSerializer(BaseTransitionSerializer):

    class Meta:
        model = SupplierCheck
        fields = ('id', 'bidding_sheet', 'applicant', 'application_dt',
                  'project', 'estimated_price', 'basic_situation', 'status')
