from rest_framework import serializers

from Procurement.models import Supplier, SupplierDocument, Quotation


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
