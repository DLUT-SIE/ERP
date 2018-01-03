from rest_framework import serializers

from Production.models import SubMaterial
from Process.serializers.process_serializers import (
    ProcessMaterialSerializer, CirculationRouteSerializer)


class SubMaterialLedgersListSerializer(serializers.ModelSerializer):
    process_material = ProcessMaterialSerializer(source='material',
                                                 read_only=True)
    circulation_route = CirculationRouteSerializer(
        source='material.circulation_route', read_only=True)

    class Meta:
        model = SubMaterial
        fields = ('id', 'process_material', 'circulation_route', 'sub_order',
                  'estimated_finish_dt', 'actual_finish_dt', 'material')
        read_only_fields = ('id', 'process_material', 'circulation_route',
                            'estimated_finish_dt', 'material', 'sub_order',
                            'actual_finish_dt')


class SubMaterialLedgersUpdateSerializer(serializers.ModelSerializer):
    inspectors = serializers.SerializerMethodField(read_only=True)
    process_material = ProcessMaterialSerializer(source='material',
                                                 read_only=True)
    circulation_route = CirculationRouteSerializer(
        source='material.circulation_route', read_only=True)
    transfercards = serializers.SerializerMethodField(read_only=True)
    process_route = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SubMaterial
        fields = ('inspectors', 'process_material', 'circulation_route',
                  'transfercards', 'process_route', 'sub_order',
                  'estimated_finish_dt', 'actual_finish_dt', 'material')
        read_only_fields = ('process_material', 'circulation_route',
                            'transfercard', 'process_route',
                            'inspector', 'material', 'sub_order',
                            'actual_finish_dt')

    def get_inspectors(self, obj):
        inspectors = []
        process_detail = obj.processdetail_set.all()
        for p in process_detail:
            inspectors.append(p.inspector.first_name if p.inspector else None)
        return inspectors

    def get_transfercards(self, obj):
        transfercards = obj.material.transfer_card
        record = {}
        for field_name in ['writer', 'write_dt', 'reviewer',
                           'review_dt', 'proofreader', 'proofread_dt',
                           'approver', 'approve_dt']:
            field_value = getattr(transfercards, field_name, None)
            record[field_name] = field_value
        return record

    def get_process_route(self, obj):
        process_steps = []
        steps = obj.material.processroute.steps.all().order_by('pk')
        for a in steps:
            step = {}
            for field_name in ['step', 'man_hours']:
                field_value = getattr(a, field_name, None)
                step[field_name] = field_value
            process_steps.append(step)
        return process_steps
