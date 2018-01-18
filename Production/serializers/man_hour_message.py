from rest_framework import serializers

from Production.models import ProcessDetail


class ManHourMessageSerializer(serializers.ModelSerializer):
    sub_order = serializers.CharField(source='sub_material.sub_order',
                                      read_only=True)
    ticket_number = serializers.CharField(
        source='sub_material.material.ticket_number', read_only=True)
    step = serializers.CharField(source='process_step.step',
                                 read_only=True)
    man_hours = serializers.CharField(source='process_step.man_hours',
                                      read_only=True)
    writer = serializers.CharField(
        source='sub_material.sub_order.work_order.process_library.writer',
        read_only=True)
    quota_clerk = serializers.CharField(
        source='sub_material.sub_order.work_order.process_library.quota_clerk',
        read_only=True)
    work_group_name = serializers.CharField(source='work_group.name',
                                            read_only=True)

    class Meta:
        model = ProcessDetail
        fields = ('id', 'sub_order', 'ticket_number', 'work_group_name',
                  'step', 'man_hours', 'writer', 'quota_clerk',
                  'actual_finish_dt')
        read_only_fields = ('id', 'work_group_name', 'actual_finish_dt')
