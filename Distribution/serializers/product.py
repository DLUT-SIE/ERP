from rest_framework import serializers

from django.db import transaction
from django.db.models import Q
from django.conf import settings

from Core.utils.fsm import TransitionSerializerMixin
from Distribution import REVIEW_STATUS_CHOICES
from Distribution.models import Product, BiddingDocument


class BiddingDocumentSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = BiddingDocument
        fields = '__all__'
        read_only_fields = ('product', 'path', 'src', 'dst', 'upload_dt')


class ProductSerializer(TransitionSerializerMixin,
                        serializers.ModelSerializer):
    documents = BiddingDocumentSerializer(many=True, read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('name', 'terminated')


class ProductListSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ('id', 'name')


class ProductUpdateSerializer(ProductSerializer):
    status = serializers.ChoiceField(choices=REVIEW_STATUS_CHOICES)

    class Meta(ProductSerializer.Meta):
        fields = ('id', 'status', 'terminated')
        read_only_fields = None


class ProductCreateSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        read_only_fields = ('status', 'terminated')


class ProductSimpleSerializer(ProductSerializer):
    documents = serializers.SerializerMethodField('get_related_documents')

    class Meta(ProductSerializer.Meta):
        fields = ('id', 'name', 'documents')
        read_only_fields = ('name', 'documents')

    def get_related_documents(self, product):
        related_id = self.context['request'].GET['related']
        documents = product.documents.filter(
            Q(src=related_id) | Q(dst=related_id))
        return BiddingDocumentSerializer(documents, many=True).data


class BiddingDocumentListSerializer(BiddingDocumentSerializer):
    class Meta(BiddingDocumentSerializer.Meta):
        fields = ('id', 'path', 'status')


class BiddingDocumentCreateSerializer(BiddingDocumentSerializer):
    class Meta(BiddingDocumentSerializer.Meta):
        fields = ('id', 'product', 'path', 'src', 'dst', 'upload_dt', 'status')
        read_only_fields = ('status', 'upload_dt')

    def validate_src(self, department):
        if settings.DEBUG is True:
            return department
        user = self.context['request'].user
        groups = user.groups.all().select_related('department')
        related_departments = [g.department for g in groups]
        if department not in related_departments:
            raise serializers.ValidationError('来源部门错误')
        return department

    def validate(self, data):
        src = data['src']
        dst = data['dst']
        if src.id == dst.id:
            raise serializers.ValidationError('来源部门与接收部门不能相同')
        data['src'] = src
        return data

    def create(self, validated_data):
        with transaction.atomic():
            product = validated_data['product']
            src = validated_data['src']
            dst = validated_data['dst']
            path = validated_data['path']
            doc, created = BiddingDocument.objects.get_or_create(
                product=product,
                src=src,
                dst=dst)
            if not created:
                doc.path.delete(save=False)
            doc.path = path
            doc.save()
        return doc
