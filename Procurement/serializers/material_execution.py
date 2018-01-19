from rest_framework import serializers
from django.db import transaction

from Procurement.models import MaterialExecution, MaterialExecutionDetail


class MaterialExecutionDetailSerializer(serializers.ModelSerializer):
    sub_order = serializers.CharField(
        source='material.sub_order', read_only=True)
    batch_number = serializers.CharField(
        source='material.batch_number', read_only=True)
    material_name = serializers.CharField(
        source='material.process_material.material.name', read_only=True)
    material_uid = serializers.CharField(
        source='material.process_material.material.uid', read_only=True)
    material_category = serializers.CharField(
        source='material.process_material.material.get_category_display',
        read_only=True)
    count = serializers.CharField(
        source='material.count', read_only=True)
    weight = serializers.CharField(
        source='material.weight', read_only=True)
    spec = serializers.CharField(
        source='material.process_material.spec', read_only=True)

    class Meta:
        model = MaterialExecutionDetail
        fields = '__all__'
        read_only_fields = ('material_execution',)


class MaterialExecutionSerializer(serializers.ModelSerializer):
    material_type = serializers.CharField(
        source='get_material_type_display', read_only=True)

    class Meta:
        model = MaterialExecution
        fields = '__all__'


class MaterialExecutionCreateSerializer(serializers.ModelSerializer):
    execution_details = MaterialExecutionDetailSerializer(many=True)

    class Meta(MaterialExecutionSerializer.Meta):
        model = MaterialExecution
        fields = '__all__'
        read_only_fields = ('lister', 'list_dt')

    def create(self, validated_data):
        with transaction.atomic():
            detail_list = validated_data.pop('execution_details')
            m_excution = MaterialExecution(lister=self.context['request'].user,
                                           **validated_data)
            m_excution.save()
            array = []
            request = self.context['request']
            for detail in detail_list:
                array.append(MaterialExecutionDetail(
                    material_execution=m_excution, **detail))
                detail['material'].material_execution_finished(request)
                detail['material'].save()
            MaterialExecutionDetail.objects.bulk_create(array)
            return m_excution


class MaterialExecutionListSerializer(MaterialExecutionSerializer):

    class Meta(MaterialExecutionSerializer.Meta):
        fields = ('id', 'uid', 'lister', 'list_dt', 'material_type',
                  'process_requirement')
