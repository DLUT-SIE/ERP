from rest_framework import serializers

from django.db import transaction

from Core.models import Department
from Core.utils.fsm import TransitionSerializerMixin
from Distribution.models import Product, BiddingDocument


class BiddingDocumentSerializer(TransitionSerializerMixin,
                                serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    name = serializers.CharField(source='path_name', read_only=True)

    class Meta:
        model = BiddingDocument
        fields = '__all__'
        read_only_fields = ('status',)

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


class BiddingDocumentSimpleSerializer(BiddingDocumentSerializer):
    class Meta(BiddingDocumentSerializer.Meta):
        fields = ('id', 'path', 'name', 'pretty_status', 'actions')


class BiddingDocumentUpdateSerializer(BiddingDocumentSerializer):
    class Meta(BiddingDocumentSerializer.Meta):
        read_only_fields = ('src', 'dst', 'product', 'path')


class ProductSerializer(TransitionSerializerMixin,
                        serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display',
                                          read_only=True)
    documents_from_distribution = serializers.SerializerMethodField()
    documents_to_distribution = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('name', 'terminated')

    @staticmethod
    def get_departments():
        dep_distribution = Department.distribution.get()
        dep_process = Department.process.get()
        dep_procurement = Department.procurement.get()
        dep_production = Department.production.get()
        return dep_distribution, dep_process, dep_procurement, dep_production

    def _get_documents(self, product, deps=None, from_distribution=True):
        documents = {}
        dep_distribution, *_deps = self.get_departments()
        if deps is None:
            deps = _deps
        candidates = BiddingDocument.objects.filter(product=product)
        if from_distribution:
            src = dep_distribution
        else:
            dst = dep_distribution
        for dep in deps:
            if from_distribution:
                dst = dep
            else:
                src = dep
            doc = candidates.filter(src=src, dst=dst)
            if doc:
                doc = BiddingDocumentSimpleSerializer(
                    doc.get(),
                    context={'request': self.context['request']}).data
            else:
                doc = None
            documents[dep.group.name] = doc
        return documents

    def get_documents_from_distribution(self, product):
        return self._get_documents(product, from_distribution=True)

    def get_documents_to_distribution(self, product):
        return self._get_documents(product, from_distribution=False)


class ProductListSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ('id', 'name', 'documents_from_distribution',
                  'documents_to_distribution')


class ProductSimpleSerializer(ProductListSerializer):
    def get_documents_from_distribution(self, product):
        related_id = self.context['request'].GET['related']
        dep = Department.objects.get(id=related_id)
        return self._get_documents(product, deps=[dep],
                                   from_distribution=True)

    def get_documents_to_distribution(self, product):
        related_id = self.context['request'].GET['related']
        dep = Department.objects.get(id=related_id)
        return self._get_documents(product, deps=[dep],
                                   from_distribution=False)


class ProductUpdateSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        read_only_fields = ('name',)


class ProductCreateSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        read_only_fields = ('status', 'terminated')
