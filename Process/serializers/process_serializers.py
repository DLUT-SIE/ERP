import ast

from rest_framework import serializers

from Process.models import (
    ProcessLibrary, ProcessMaterial, CirculationRoute, ProcessRoute,
    ProcessStep)


class ProcessLibrarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='work_order.product.name')
    status = serializers.SerializerMethodField()
    work_order_uid = serializers.CharField(source='work_order.uid')

    class Meta:
        model = ProcessLibrary
        fields = ('id', 'proofreader', 'writer', 'status', 'name',
                  'work_order_uid')
        read_only_fields = ('status', 'name', 'work_order_uid')

    def get_status(self, obj):
        if obj.process_materials.count() == 0:
            return 0
        elif obj.writer is not None:
            return 2
        return 1


class ProcessMaterialSerializer(serializers.ModelSerializer):
    total_weight = serializers.SerializerMethodField()

    class Meta:
        model = ProcessMaterial
        fields = '__all__'

    def get_total_weight(self, obj):
        if obj.piece_weight:
            return obj.piece_weight * obj.count
        return 0


class CirculationRouteSerializer(serializers.ModelSerializer):
    circulation_routes = serializers.SerializerMethodField()

    class Meta:
        model = CirculationRoute
        fields = ('id', 'process_material', 'circulation_routes')

    def get_circulation_routes(self, obj):
        circulation_routes = []
        for i in range(10):
            cur = getattr(obj, 'C{}'.format(i + 1))
            if not cur:
                break
            circulation_routes.append(cur)
        return circulation_routes

    def update(self, instance, validated_data):
        circulation_routes = validated_data['circulation_routes']
        for index, item in enumerate(circulation_routes):
            setattr(instance, 'C{}'.format(index + 1), item)
        instance.save()
        return instance

    def validate(self, attrs):
        data = self.context['request'].data
        if 'circulation_routes' not in data:
            raise serializers.ValidationError("流转路线为空")
        attrs['circulation_routes'] = ast.literal_eval(
            data['circulation_routes'])
        return attrs


class ProcessRouteSerializer(serializers.ModelSerializer):
    process_steps = serializers.SerializerMethodField()

    class Meta:
        model = ProcessRoute
        fields = ('id', 'process_steps', 'process_material')

    def get_process_steps(self, obj):
        steps = obj.steps
        process_steps = []
        for step in steps.all().order_by('pk'):
            process_steps.append(step.step)
        return process_steps

    def update(self, instance, validated_data):
        instance.steps.all().delete()
        process_steps = validated_data['process_steps']
        steps = []
        for step in process_steps:
            steps.append(ProcessStep(route=instance, step=step))
        ProcessStep.objects.bulk_create(steps)
        instance.save()
        return instance

    def validate(self, attrs):
        data = self.context['request'].data
        if 'process_steps' not in data:
            raise serializers.ValidationError("工序路线为空")
        attrs['process_steps'] = ast.literal_eval(
            data['process_steps'])
        return attrs
