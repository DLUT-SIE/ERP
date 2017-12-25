import ast

from rest_framework import serializers

from Process.models import (
    ProcessLibrary, ProcessMaterial, CirculationRoute, ProcessRoute,
    ProcessStep, TransferCard, TransferCardProcess, BoughtInItem,
    FirstFeedingItem, CooperantItem, AbstractQuotaItem)


class GetCirculationRoutesMixin(serializers.Serializer):
    circulation_routes = serializers.SerializerMethodField(read_only=True)

    def get_circulation_routes(self, obj):
        circulation_routes = []
        routes = obj.process_material.circulation_route
        for i in range(10):
            cur = getattr(routes, 'C{}'.format(i + 1))
            if not cur:
                break
            name = getattr(routes, 'get_C{}_display'.format(i + 1))()
            circulation_routes.append(name)
        return circulation_routes


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
    material = serializers.CharField(source='material.name')

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
        circulation_routes = [circulation_routes] if isinstance(
            circulation_routes, int) else circulation_routes
        circulation_routes.extend([None] * (10 - len(circulation_routes)))
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
        process_steps = [process_steps] if isinstance(process_steps, int) \
            else process_steps
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


class TransferCardListSerializer(serializers.ModelSerializer):
    ticket_number = serializers.IntegerField(
        source='process_material.ticket_number', read_only=True)
    name = serializers.CharField(source='process_material.name',
                                 read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    file_index = serializers.SerializerMethodField(read_only=True)
    category = serializers.CharField(source='get_category_display')

    class Meta:
        model = TransferCard
        fields = ('id', 'category', 'name', 'ticket_number', 'status',
                  'file_index')

    def get_status(self, obj):
        return obj.status

    def get_file_index(self, obj):
        return str(obj)


class TransferCardSerializer(GetCirculationRoutesMixin,
                             TransferCardListSerializer):
    basic_file = serializers.CharField(source='basic_file_name',
                                       read_only=True)
    work_order_uid = serializers.CharField(
        source='process_material.lib.work_order.uid', read_only=True)
    product_name = serializers.CharField(
        source='process_material.lib.work_order.product', read_only=True)
    parent_drawing_number = serializers.CharField(
        source='process_material.parent_drawing_number', read_only=True)
    count = serializers.IntegerField(source='process_material.count',
                                     read_only=True)

    press_mark = serializers.CharField(source='process_material.remark',
                                       read_only=True)
    material = serializers.CharField(source='process_material.material.name',
                                     read_only=True)
    drawing_number = serializers.CharField(
        source='process_material.drawing_number', read_only=True)
    circulation_routes = serializers.SerializerMethodField(read_only=True)

    class Meta(TransferCardListSerializer.Meta):
        fields = '__all__'


class TransferCardProcessSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransferCardProcess
        fields = '__all__'


class AbstractQuotaItemSerializer(GetCirculationRoutesMixin,
                                  serializers.ModelSerializer):
    ticket_number = serializers.IntegerField(
        source='process_material.ticket_number')
    drawing_number = serializers.CharField(
        source='process_material.drawing_number', read_only=True)
    name = serializers.CharField(source='process_material.name',
                                 read_only=True)
    count = serializers.IntegerField(source='process_material.count',
                                     read_only=True)
    piece_weight = serializers.FloatField(
        source='process_material.piece_weight', read_only=True)
    total_weight = serializers.SerializerMethodField()
    material = serializers.CharField(source='process_material.material.name',
                                     read_only=True)
    writer = serializers.CharField(source='quota_list.writer.first_name',
                                   allow_null=True, read_only=True)
    reviewer = serializers.CharField(source='quota_list.reviewer.first_name',
                                     allow_null=True, read_only=True)
    product_name = serializers.CharField(
        source='process_material.lib.work_order.product', read_only=True)
    work_order_uid = serializers.CharField(
        source='process_material.lib.work_order.uid')

    class Meta:
        model = AbstractQuotaItem
        fields = ('id', 'ticket_number', 'drawing_number', 'name',
                  'product_name', 'count', 'material',
                  'piece_weight', 'total_weight', 'writer', 'reviewer',
                  'quota_list', 'work_order_uid', 'circulation_routes',
                  'remark')

    def get_total_weight(self, obj):
        piece_weight = obj.process_material.piece_weight
        if piece_weight:
            return piece_weight * obj.process_material.count
        return 0

    def create(self, validated_data):
        ticket_number = validated_data['process_material']['ticket_number']
        quota_list = validated_data['quota_list']
        work_order_uid = validated_data['uid']
        process_material = ProcessMaterial.objects.get(
            ticket_number=ticket_number,
            lib__work_order__uid=work_order_uid)
        quota_item = self.Meta.model.objects.create(
            quota_list=quota_list, process_material=process_material)
        return quota_item

    def validate(self, attrs):
        ticket_number = attrs['process_material']['ticket_number']
        work_order_uid =\
            attrs['process_material']['lib']['work_order']['uid']
        quota_list = attrs['quota_list']
        attrs['uid'] = work_order_uid
        attrs['ticket_number'] = ticket_number
        process_material = ProcessMaterial.objects.filter(
            ticket_number=ticket_number,
            lib__work_order__uid=work_order_uid)
        if not process_material:
            raise serializers.ValidationError("创建信息有误，请核对")
        else:
            process_material = process_material[0]

        if self.Meta.model.objects.filter(
                quota_list=quota_list, process_material=process_material)\
                .count():
            raise serializers.ValidationError("该条物料已经添加")
        return attrs


class AbstractQuotaItemUpdateSerializer(AbstractQuotaItemSerializer):
    ticket_number = serializers.IntegerField(
        source='process_material.ticket_number', read_only=True)
    work_order_uid = serializers.CharField(
        source='process_material.lib.work_order.uid', read_only=True)


class FirstFeedingItemSerializer(AbstractQuotaItemSerializer):
    class Meta(AbstractQuotaItemSerializer.Meta):
        model = FirstFeedingItem


class FirstFeedingItemUpdateSerializer(AbstractQuotaItemUpdateSerializer):
    class Meta(AbstractQuotaItemUpdateSerializer.Meta):
        model = FirstFeedingItem


class CooperantItemSerializer(AbstractQuotaItemSerializer):
    class Meta(AbstractQuotaItemSerializer.Meta):
        model = CooperantItem


class CooperantItemUpdateSerializer(AbstractQuotaItemUpdateSerializer):
    class Meta(AbstractQuotaItemUpdateSerializer.Meta):
        model = CooperantItem


class BoughtInItemSerializer(AbstractQuotaItemSerializer):
    class Meta(AbstractQuotaItemSerializer.Meta):
        model = BoughtInItem


class BoughtInItemUpdateSerializer(AbstractQuotaItemUpdateSerializer):
    class Meta(AbstractQuotaItemUpdateSerializer.Meta):
        model = BoughtInItem
