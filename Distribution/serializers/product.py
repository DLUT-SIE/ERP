from rest_framework import serializers

from Distribution.models import Product, BiddingDocument


class ProductSerializer(serializers.ModelSerializer):
    documents = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('name',)


class ProductListSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ('id', 'name')


class ProductCreateSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        read_only_fields = ('status', 'terminated')


class BiddingDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingDocument
        fields = '__all__'
        read_only_fields = ('product', 'path', 'src', 'dst')


class BiddingDocumentListSerializer(BiddingDocumentSerializer):
    class Meta(BiddingDocumentSerializer.Meta):
        fields = ('id', 'path', 'status')


class BiddingDocumentCreateSerializer(BiddingDocumentSerializer):
    class Meta(BiddingDocumentSerializer.Meta):
        read_only_fields = ('status',)
