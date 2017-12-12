from rest_framework import serializers

from Procurement.models import MaterialSubApply, MaterialSubApplyItems


class MaterialSubApplyItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialSubApplyItems
        fields = '__all__'
        read_only_fields = ('sub_apply',)


class MaterialSubApplyItemsCreateSerializer(MaterialSubApplyItemsSerializer):
    class Meta(MaterialSubApplyItemsSerializer.Meta):
        fields = '__all__'
        read_only_fields = ()


class MaterialSubApplySerializer(serializers.ModelSerializer):

    items = MaterialSubApplyItemsSerializer(many=True, read_only=True)

    class Meta:
        model = MaterialSubApply
        fields = '__all__'
        read_only_fields = ('uid', 'applicant')


class MaterialSubApplyListSerializer(MaterialSubApplySerializer):
    class Meta(MaterialSubApplySerializer.Meta):
        fields = ('uid', 'production')


class MaterialSubApplyCreateSerializer(MaterialSubApplySerializer):
    class Meta(MaterialSubApplySerializer.Meta):
        fields = '__all__'
        read_only_fields = ('applicant', )

    def perform_create(self, serializer):
        serializer.save(applicant=self.context['request'].user)
