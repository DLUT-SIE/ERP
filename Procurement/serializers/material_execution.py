from rest_framework import serializers
from django.db import transaction

from Procurement.models import MaterialExecution, MaterialExecutionDetail


class MaterialExecutionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialExecutionDetail
        fields = '__all__'


class MaterialExecutionSerializer(serializers.ModelSerializer):

    materialexecution = MaterialExecutionDetailSerializer(many=True)

    # TODO: 此处是物料的外接显示，等待武指导写完物料的序列化器引入即可

    class Meta:
        model = MaterialExecution
        fields = '__all__'


class MaterialExecutionCreateSerializer(serializers.ModelSerializer):

    details = serializers.ListField(
        child=serializers.IntegerField(), write_only=True)

    class Meta(MaterialExecutionSerializer.Meta):
        model = MaterialExecution
        fields = '__all__'
        read_only_fields = ('lister',)

    def create(self, validated_data):
        with transaction.atomic():
            id_array = validated_data.pop('details')
            m_excution = MaterialExecution(lister=self.context['request'].user,
                                           **validated_data)
            m_excution.save()
            MaterialExecutionDetail.objects.filter(
                id__in=id_array).update(material_execution=m_excution)
        return m_excution


class MaterialExecutionListSerializer(MaterialExecutionSerializer):

    class Meta(MaterialExecutionSerializer.Meta):
        fields = ('uid', 'lister', 'list_dt', 'material_type',
                  'process_requirement')
