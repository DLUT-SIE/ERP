from rest_framework import serializers

from Core.utils.fsm import TransitionSerializerMixin
from Production.models import (ProcessDetail,
                               SubMaterial,
                               ProductionWorkGroup)


class ProcessDetailSerializer(TransitionSerializerMixin,
                              serializers.ModelSerializer):
    material_index = serializers.CharField(
        source='sub_material.material.ticket_number', read_only=True)
    work_order_uid = serializers.CharField(source='sub_material.sub_order',
                                           read_only=True)
    process_id = serializers.IntegerField(source='process_step.step',
                                          read_only=True)
    process_name = serializers.CharField(
        source='process_step.get_step_display', read_only=True)
    work_hour = serializers.FloatField(source='process_step.man_hours',
                                       read_only=True)
    work_group_name = serializers.CharField(source='work_group.name',
                                            allow_null=True, read_only=True)
    inspector_name = serializers.CharField(source='inspector.username',
                                           allow_null=True, read_only=True)

    class Meta:
        model = ProcessDetail
        fields = ('id', 'sub_material', 'material_index', 'work_order_uid',
                  'process_step', 'process_id', 'process_name', 'work_hour',
                  'estimated_start_dt', 'estimated_finish_dt', 'work_group',
                  'work_group_name', 'actual_finish_dt', 'remark',
                  'inspector', 'inspector_name', 'inspection_dt', 'status')


class ProcessDetailCreateSerializer(ProcessDetailSerializer):
    class Meta(ProcessDetailSerializer.Meta):
        read_only_fields = ('estimated_start_dt', 'estimated_finish_dt',
                            'work_group', 'actual_finish_dt', 'remark',
                            'inspector', 'inspection_dt')


class ProcessDetailListSerializer(ProcessDetailSerializer):
    select_work_groups = serializers.SerializerMethodField()

    class Meta(ProcessDetailSerializer.Meta):
        fields = ('id', 'material_index', 'work_order_uid', 'process_id',
                  'process_name', 'work_hour', 'estimated_start_dt',
                  'estimated_finish_dt', 'work_group', 'work_group_name',
                  'select_work_groups', 'actual_finish_dt', 'inspection_dt',
                  'status')

    def get_select_work_groups(self, obj):
        work_groups = ProductionWorkGroup.objects.filter(
            process=obj.process_step.step).values('id', 'name')
        return work_groups


class ProcessDetailSimpleSerializer(ProcessDetailSerializer):
    class Meta(ProcessDetailSerializer.Meta):
        read_only_fields = ('sub_material', 'process_step', 'actual_finish_dt',
                            'inspector', 'inspection_dt')


class SubMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMaterial
        fields = ('id', 'material', 'sub_order',
                  'estimated_finish_dt', 'actual_finish_dt')
        read_only_fields = ('material', 'sub_order')


class SubMaterialCreateSerializer(SubMaterialSerializer):
    class Meta(SubMaterialSerializer.Meta):
        read_only_fields = ('estimated_finish_dt', 'actual_finish_dt')
