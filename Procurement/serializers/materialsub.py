from rest_framework import serializers

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

    sub_apply_items = MaterialSubApplyItemsSerializer(many=True,
                                                      read_only=True)
    sub_spply_comments = MaterialSubApplyCommentsSerializer(many=True,
                                                            read_only=True)

    class Meta:
        model = MaterialSubApply
        fields = '__all__'
        read_only_fields = ('applicant',)


class MaterialSubApplyListSerializer(MaterialSubApplySerializer):
    class Meta(MaterialSubApplySerializer.Meta):
        fields = ('id', 'uid', 'work_order', 'production', 'figure_code',
                  'applicant', 'reason',)
