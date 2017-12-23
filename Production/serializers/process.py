from rest_framework import serializers

from Production.models import ProcessDetail, SubMaterial


class ProcessDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessDetail
        fields = ('id', 'sub_material', 'process_step')


class ProcessDetailSerializer(serializers.ModelSerializer):
    material_index = serializers.CharField(
        source='sub_material.material.ticket_number', read_only=True)
    work_order_uid = serializers.CharField(source='sub_material.sub_order',
                                           read_only=True)
    process_id = serializers.IntegerField(source='process_step.step',
                                          read_only=True)
    process_name = serializers.CharField(
        source='process_step.get_step_display', read_only=True)
    work_hour = serializers.FloatField(source='process_step.man_hour',
                                       read_only=True)

    class Meta:
        model = ProcessDetail
        fields = ('id', 'material_index', 'work_order_uid', 'process_id',
                  'process_name', 'work_hour', 'estimated_start_dt',
                  'estimated_finish_dt', 'work_group', 'actual_finish_dt',
                  'remark', 'inspector', 'inspection_dt')


class ProcessDetailListSerializer(ProcessDetailSerializer):
    class Meta(ProcessDetailSerializer.Meta):
        fields = ('id', 'material_index', 'work_order_uid', 'process_id',
                  'process_name', 'work_hour', 'estimated_start_dt',
                  'estimated_finish_dt', 'work_group', 'actual_finish_dt',
                  'inspection_dt')


class SubMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMaterial
        fields = '__all__'
        read_only_fields = ('material', 'sub_order')


class SubMaterialCreateSerializer(SubMaterialSerializer):
    class Meta(SubMaterialSerializer.Meta):
        read_only_fields = ('estimated_finish_dt', 'actual_finish_dt')
