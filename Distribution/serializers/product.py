from rest_framework import serializers

from Core.models import Department
from Core.utils.fsm import TransitionSerializerMixin
from Distribution import BIDDING_DOC_UPLOAD_TYPE_CHOICES
from Distribution.models import Product, BiddingDocument


class ProductSerializer(TransitionSerializerMixin,
                        serializers.ModelSerializer):
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
        read_only_fields = ('product', 'path', 'src', 'dst', 'upload_dt')


class BiddingDocumentListSerializer(BiddingDocumentSerializer):
    class Meta(BiddingDocumentSerializer.Meta):
        fields = ('id', 'path', 'status')


class BiddingDocumentCreateSerializer(BiddingDocumentSerializer):
    category = serializers.ChoiceField(label='文件类型',
                                       choices=BIDDING_DOC_UPLOAD_TYPE_CHOICES)

    class Meta(BiddingDocumentSerializer.Meta):
        fields = ('id', 'product', 'path', 'category', 'upload_dt', 'status')
        read_only_fields = ('status', 'upload_dt')

    def create(self, validated_data):
        product = validated_data['product']
        fpath = validated_data['path']
        category = validated_data['category']
        # TODO: **IMPORTANT** Delete these debug code,
        # and come up with a new plan
        if category < 3:
            src = 0
            dst = category + 1
        else:
            dst = 0
            src = category - 2
        src = Department.objects.all()[src]
        dst = Department.objects.all()[dst]
        doc, created = BiddingDocument.objects.get_or_create(
            product=product,
            src=src,
            dst=dst)
        if not created:
            doc.path.delete(save=False)
        doc.path = fpath
        doc.save()
        doc.category = category
        return doc
