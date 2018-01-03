from rest_framework import serializers
from django.db import transaction

from Procurement.models import MaterialExecution, MaterialExecutionDetail
from Procurement.serializers import ProcurementMaterialReadSerializer


class MaterialExecutionDetailSerializer(serializers.ModelSerializer):
    material = ProcurementMaterialReadSerializer(read_only=True)

    class Meta:
        model = MaterialExecutionDetail
        fields = '__all__'


class MaterialExecutionSerializer(serializers.ModelSerializer):
    materialexecution = MaterialExecutionDetailSerializer(many=True)

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
