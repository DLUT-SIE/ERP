from rest_framework import serializers
from django.db import transaction

from Procurement.models import MaterialSubApply, MaterialSubApplyItems
from Procurement.models import SubApplyComment


class MaterialSubApplyItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialSubApplyItems
        fields = '__all__'


class MaterialSubApplyItemsUpdateSerializer(MaterialSubApplyItemsSerializer):
    class Meta(MaterialSubApplyItemsSerializer.Meta):
        fields = '__all__'
        read_only_fields = ('sub_apply',)


class MaterialSubApplyCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubApplyComment
        fields = '__all__'
        read_only_fields = ('user',)


class MaterialSubApplySerializer(serializers.ModelSerializer):

    sub_apply_items = MaterialSubApplyItemsUpdateSerializer(many=True)
    sub_spply_comments = MaterialSubApplyCommentsSerializer(many=True,
                                                            read_only=True)

    class Meta:
        model = MaterialSubApply
        fields = '__all__'
        read_only_fields = ('applicant',)

    def create(self, validated_data):
        with transaction.atomic():
            item_list = validated_data.pop('sub_apply_items')
            m_subapply = MaterialSubApply(
                applicant=self.context['request'].user,
                **validated_data)
            m_subapply.save()
            items = []
            for item in item_list:
                items.append(MaterialSubApplyItems(
                    sub_apply=m_subapply, **item))
            MaterialSubApplyItems.objects.bulk_create(items)
            return m_subapply


class MaterialSubApplyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialSubApply
        fields = ('figure_code', 'work_order', 'production', 'reason')


class MaterialSubApplyListSerializer(MaterialSubApplySerializer):
    class Meta(MaterialSubApplySerializer.Meta):
        fields = ('id', 'uid', 'work_order', 'production', 'figure_code',
                  'applicant', 'reason',)
