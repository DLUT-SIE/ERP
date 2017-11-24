from rest_framework import serializers

from Distribution.models import Product, BiddingDocument


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BiddingDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingDocument
        fields = '__all__'
