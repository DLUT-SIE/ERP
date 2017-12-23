from rest_framework import serializers

from Procurement.models import MaterialExecution, MaterialExecutionDetail


class MaterialExecutionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialExecutionDetail
        fields = '__all__'


class MaterialExecutionSerializer(serializers.ModelSerializer):

    materialexecution = MaterialExecutionDetailSerializer(many=True,
                                                          read_only=True)

    # TODO: 此处是物料的外接显示，等待武指导写完物料的序列化器引入即可

    class Meta:
        model = MaterialExecution
        fields = '__all__'


class MaterialExecutionCreateSerializer(MaterialExecutionSerializer):

    # TODO: 此处待完善，创建时需要完成对材料执行明细表的绑定

    class Meta(MaterialExecutionSerializer.Meta):
        fields = '__all__'
        read_only_fields = ('lister',)


class MaterialExecutionListSerializer(MaterialExecutionSerializer):

    class Meta(MaterialExecutionSerializer.Meta):
        fields = ('uid', 'lister', 'list_dt', 'material_type',
                  'process_requirement')
