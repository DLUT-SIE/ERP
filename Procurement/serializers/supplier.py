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

    class Meta:
        model = SupplierDocument
        fields = '__all__'


class QuotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quotation
        fields = '__all__'


class SupplierListSerializer(SupplierSerializer):
    doc = SupplierDocumentSerializer(read_only=True, many=True)

    class Meta(SupplierSerializer.Meta):
        fields = '__all__'


class SupplierDetailSerializer(SupplierSerializer):
    doc = SupplierDocumentSerializer(read_only=True, many=True)
    quotation = QuotationSerializer(read_only=True, many=True)

    class Meta(SupplierSerializer.Meta):
        fields = '__all__'


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
