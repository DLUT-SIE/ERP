from rest_framework import serializers

from Production.models import SubMaterial
from Process.serializers.process_serializers import (
    ProcessMaterialSerializer, CirculationRouteSerializer,
    ProcessRouteSerializer)


class SubMaterialLedgersListSerializer(serializers.ModelSerializer):
    process_material = ProcessMaterialSerializer(source='material',
                                                 read_only=True)
    circulation_route = CirculationRouteSerializer(
        source='material.circulation_route', read_only=True)

    class Meta:
        model = SubMaterial
        fields = '__all__'
        read_only_fields = ('process_material', 'circulation_route',
                            'estimated_finish_dt', 'material', 'sub_order',
                            'actual_finish_dt')


class SubMaterialLedgersUpdateSerializer(serializers.ModelSerializer):
    inspectors = serializers.SerializerMethodField(read_only=True)
    process_material = ProcessMaterialSerializer(source='material',
                                                 read_only=True)
    circulation_route = CirculationRouteSerializer(
        source='material.circulation_route', read_only=True)
    transfercards = serializers.SerializerMethodField(read_only=True)
    process_route = ProcessRouteSerializer(source='material.processroute',
                                           read_only=True)

    class Meta:
        model = SubMaterial
        fields = '__all__'
        read_only_fields = ('process_material', 'circulation_route',
                            'transfercard', 'process_route',
                            'inspector', 'material', 'sub_order',
                            'actual_finish_dt')

    def get_inspectors(self, obj, *args):
        inspectors = []
        process_detail = obj.processdetail_set.all()
        for p in process_detail:
            inspectors.append(p.inspector.first_name if p.inspector else None)
        return inspectors

    def get_transfercards(self, obj, *args):
        cards = []
        transfercards = obj.material.transfercard_set.all()
        for a in transfercards:
            record = {}
            for field_name in ['writer', 'write_dt', 'reviewer',
                               'review_dt', 'proofreader', 'proofread_dt',
                               'approver', 'approve_dt']:
                field_value = getattr(a, field_name, None)
                record[field_name] = field_value
            cards.append(record)
        return cards
