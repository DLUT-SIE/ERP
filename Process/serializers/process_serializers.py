from django.db import transaction
from django.db.models import F
from rest_framework import serializers
from Process.models import (
    ProcessLibrary, ProcessMaterial, CirculationRoute, ProcessRoute,
    ProcessStep, TransferCard, TransferCardProcess, BoughtInItem, QuotaList,
    FirstFeedingItem, CooperantItem, AbstractQuotaItem, PrincipalQuotaItem,
    WeldingQuotaItem, Material, AuxiliaryQuotaItem, WeldingSeam,
    TotalWeldingMaterial, WeldingMaterial, FluxMaterial, WeldingCertification,
    WeldingProcessSpecification, WeldingJointProcessAnalysis,
    WeldingWorkInstruction)
from Core.utils.fsm import TransitionSerializerMixin as TSMixin


class GetCirculationRoutesMixin(serializers.Serializer):
    circulation_routes = serializers.SerializerMethodField()

    def get_circulation_routes(self, obj):
        circulation_routes = []
        if hasattr(obj.process_material, 'circulation_route'):
            return None
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
    material = serializers.CharField(source='material.name', default='')
    transfer_card_id = serializers.IntegerField(source='transfer_card.id')
    transfer_card_name = serializers.CharField(
        source='transfer_card.get_category_display')

    class Meta:
        model = ProcessMaterial
        fields = '__all__'

    def get_total_weight(self, obj):
        if obj.piece_weight:
            return obj.piece_weight * obj.count
        return 0


class CirculationRouteSerializer(serializers.ModelSerializer):
    circulation_routes = serializers.SerializerMethodField(allow_null=True)

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
        circulation_routes = list(circulation_routes)
        circulation_routes.extend([None] * (10 - len(circulation_routes)))
        for index, item in enumerate(circulation_routes):
            setattr(instance, 'C{}'.format(index + 1), item)
        instance.save()
        return instance

    def validate(self, attrs):
        viewset = self.context['view']
        if viewset.action not in ['update', 'partial_update']:
            return attrs
        data = self.context['request'].data
        if 'circulation_routes' not in data:
            raise serializers.ValidationError("流转路线为空")
        attrs['circulation_routes'] = data['circulation_routes']
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
        attrs['process_steps'] = data['process_steps']
        return attrs


class TransferCardCreateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='get_category_display',
                                          read_only=True)

    def validate_process_material(self, value):
        if ProcessMaterial.objects.filter(id=value.id).exists():
            return value
        raise serializers.ValidationError("请传入正确的工艺物料")

    class Meta:
        model = TransferCard
        fields = '__all__'
        read_only_fields = ('container_category', 'parent_name',
                            'welding_plate_idx', 'parent_plate_idx',
                            'material_index', 'path', 'tech_requirement',
                            'writer', 'write_dt', 'reviewer', 'review_dt',
                            'proofreader', 'proofread_dt', 'approver',
                            'approve_dt', 'file_index', 'category_name')


class TransferCardListSerializer(serializers.ModelSerializer):
    ticket_number = serializers.IntegerField(
        source='process_material.ticket_number', read_only=True)
    name = serializers.CharField(source='process_material.name',
                                 read_only=True)
    status = serializers.SerializerMethodField()
    file_index = serializers.SerializerMethodField()
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
    circulation_routes = serializers.SerializerMethodField()

    class Meta(TransferCardListSerializer.Meta):
        fields = '__all__'


class TransferCardProcessSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransferCardProcess
        fields = '__all__'

    def create(self, validated_data):
        transfer_card = validated_data['transfer_card']
        index = validated_data['index']
        transfer_card_processes = TransferCardProcess.objects.filter(
            index__gte=index, transfer_card=transfer_card)
        with transaction.atomic():
            transfer_card_processes.update(index=F('index')+1)
            return TransferCardProcess.objects.create(**validated_data)


class TransferCardProcessUpdateSerializer(serializers.ModelSerializer):
    direction = serializers.IntegerField(write_only=True)

    class Meta:
        model = TransferCardProcess
        fields = '__all__'

    def update(self, instance, validated_data):
        direction = validated_data.get('direction')
        with transaction.atomic():
            if direction == 0:
                pre = TransferCardProcess.objects\
                    .filter(transfer_card=instance.transfer_card).filter(
                        index=instance.index-1)
                pre.update(index=F('index')+1)
                validated_data['index'] = instance.index - 1

            elif direction == 1:
                next = TransferCardProcess.objects \
                    .filter(transfer_card=instance.transfer_card).filter(
                        index=instance.index+1)
                next.update(index=F('index')-1)
                validated_data['index'] = instance.index + 1
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            return instance


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

    class Meta:
        model = AbstractQuotaItem
        fields = ('id', 'ticket_number', 'drawing_number', 'name', 'count',
                  'material', 'piece_weight', 'total_weight', 'quota_list',
                  'circulation_routes', 'remark')

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
        viewset = self.context['view']
        if viewset.action in ['update', 'partial_update']:
            return attrs
        ticket_number = attrs['process_material']['ticket_number']
        work_order_uid = attrs['quota_list'].lib.work_order.uid
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
                process_material=process_material).exists():
            raise serializers.ValidationError("该条物料已经添加")
        return attrs


class AbstractQuotaItemUpdateSerializer(AbstractQuotaItemSerializer):
    ticket_number = serializers.IntegerField(
        source='process_material.ticket_number', read_only=True)


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


class PrincipalQuotaItemSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', default=None,
                                          read_only=True)
    total_weight = serializers.SerializerMethodField()

    class Meta:
        model = PrincipalQuotaItem
        fields = ('id', 'material_name', 'total_weight', 'size', 'count',
                  'weight', 'operative_norm', 'status', 'remark', 'material')

    def get_total_weight(self, obj):
        if obj.weight:
            return obj.count * obj.weight
        return 0


class QuotaListSerializer(TSMixin, serializers.ModelSerializer):
    product_name = serializers.CharField(source='lib.work_order.product',
                                         read_only=True)
    work_order_uid = serializers.CharField(source='lib.work_order.uid',
                                           read_only=True)
    writer = serializers.CharField(source='writer.first_name',
                                   allow_null=True, read_only=True)
    reviewer = serializers.CharField(source='reviewer.first_name',
                                     allow_null=True, read_only=True)

    class Meta:
        model = QuotaList
        fields = ('id', 'status', 'actions', 'writer', 'reviewer',
                  'product_name', 'work_order_uid')


class PrincipalQuotaItemCreateSerializer(PrincipalQuotaItemSerializer):
    class Meta:
        model = PrincipalQuotaItem
        fields = ('id', 'material_name', 'total_weight', 'size', 'count',
                  'weight', 'operative_norm', 'status', 'remark', 'material',
                  'quota_list')

    def get_total_weight(self, obj):
        if obj.weight:
            return obj.count * obj.weight
        return 0


class WeldingQuotaItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='material.get_category_display',
                                     read_only=True)
    material_name = serializers.CharField(source='material.name',
                                          read_only=True)

    class Meta:
        model = WeldingQuotaItem
        fields = ('id', 'category', 'material', 'size', 'operative_norm',
                  'remark', 'material_name', 'quota')


class WeldingQuotaItemCreateSerializer(WeldingQuotaItemSerializer):
    class Meta:
        model = WeldingQuotaItem
        fields = ('id', 'category', 'material', 'size', 'operative_norm',
                  'quota_list', 'remark', 'material_name', 'quota')


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = '__all__'


class AuxiliaryQuotaItemListSerializer(AbstractQuotaItemSerializer):
    parent_drawing_number = serializers.CharField(
        source='process_material.parent_drawing_number', read_only=True)
    spec = serializers.CharField(source='process_material.spec',
                                 read_only=True)
    press_mark = serializers.CharField(source='process_material.remark',
                                       read_only=True)
    use_ratio = serializers.SerializerMethodField()

    def get_use_ratio(self, obj):
        if obj.process_material.piece_weight and obj.quota:
            return obj.quota / obj.process_material.piece_weight * 100
        return 0

    class Meta(AbstractQuotaItemSerializer.Meta):
        model = AuxiliaryQuotaItem

        # TODO: 毛重属性绑定有问题
        fields = ('id', 'ticket_number', 'parent_drawing_number',
                  'drawing_number', 'category', 'material', 'spec', 'count',
                  'piece_weight', 'total_weight', 'quota', 'use_ratio',
                  'press_mark')


class AuxiliaryQuotaItemSerializer(AuxiliaryQuotaItemListSerializer):
    name = serializers.CharField(source='process_material.name',
                                 read_only=True)
    ticket_number = serializers.IntegerField(
        source='process_material.ticket_number', read_only=True)

    class Meta(AuxiliaryQuotaItemListSerializer.Meta):
        fields = ('id', 'ticket_number', 'drawing_number', 'name',
                  'press_mark', 'material', 'count', 'piece_weight',
                  'total_weight', 'spec', 'quota_coef', 'quota',
                  'stardard_code', 'remark', 'category')


class AuxiliaryQuotaItemCreateSerializer(AuxiliaryQuotaItemSerializer):
    ticket_number = serializers.IntegerField(
        source='process_material.ticket_number')

    class Meta(AuxiliaryQuotaItemSerializer.Meta):
        fields = ('id', 'ticket_number', 'drawing_number', 'name',
                  'press_mark', 'material', 'count', 'piece_weight',
                  'total_weight', 'spec', 'quota_coef', 'quota',
                  'stardard_code', 'remark', 'category', 'quota_list')
        read_only_fields = ('quota_coef', 'quota', 'stardard_code', 'remark',
                            'category')


class WeldingSeamSerializer(serializers.ModelSerializer):
    weld_position_name = serializers.CharField(
        source='get_weld_position_display', read_only=True)
    weld_method_1_name = serializers.CharField(
        source='get_weld_method_1_display', read_only=True)
    weld_method_2_name = serializers.CharField(
        source='get_weld_method_2_display', read_only=True)
    added_welding_joint = serializers.SerializerMethodField()

    def get_added_welding_joint(self, obj):
        return obj.analysis is not None

    class Meta:
        model = WeldingSeam
        exclude = ('analysis', )


class WeldingSeamListSerializer(WeldingSeamSerializer):
    drawing_number = serializers.CharField(
        source='process_material.drawing_number')
    ticket_number = serializers.IntegerField(
        source='process_material.ticket_number')
    wm_1_name = serializers.SerializerMethodField()
    wm_2_name = serializers.SerializerMethodField()
    wf_1_name = serializers.SerializerMethodField()
    wf_2_name = serializers.SerializerMethodField()

    # TODO: 母材是否绑定材质表？

    def get_wm_1_name(self, obj):
        if obj.wm_1:
            return obj.wm_1.name
        return None

    def get_wm_2_name(self, obj):
        if obj.wm_2:
            return obj.wm_2.name
        return None

    def get_wf_1_name(self, obj):
        if obj.wf_1:
            return obj.wf_1.name
        return None

    def get_wf_2_name(self, obj):
        if obj.wf_2:
            return obj.wf_2.name
        return None

    class Meta:
        model = WeldingSeam
        fields = ('id', 'added_welding_joint', 'drawing_number',
                  'ticket_number', 'uid', 'seam_type', 'weld_position_name',
                  'weld_method_1_name', 'weld_method_2_name', 'bm_1',
                  'bm_thick_1', 'bm_2', 'bm_thick_2', 'length', 'wm_1', 'wf_1',
                  'wt_1', 'ws_1', 'weight_1', 'wf_weight_1', 'wm_2', 'wf_2',
                  'wt_2', 'ws_2', 'weight_2', 'wf_weight_2', 'remark',
                  'wm_1_name', 'wm_2_name', 'wf_1_name', 'wf_2_name')


class TotalWeldingMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = TotalWeldingMaterial
        fields = '__all__'


class WeldingMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeldingMaterial
        fields = '__all__'


class FluxMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = FluxMaterial
        fields = '__all__'


class WeldingProcessSpecificationSerializer(serializers.ModelSerializer):
    uid = serializers.SerializerMethodField()
    product = serializers.CharField(source='work_order.product.name',
                                    read_only=True)
    project = serializers.CharField(source='work_order.project',
                                    read_only=True)
    drawing_number = serializers.SerializerMethodField()

    def get_drawing_number(self, obj):
        lib = obj.work_order.process_library
        process_material = ProcessMaterial.objects.filter(lib=lib)\
            .order_by('pk')
        if not process_material:
            return ''
        return process_material[0].drawing_number

    def get_uid(self, obj):
            header = 'RH09'
            return '{}-{}'.format(header,
                                  obj.work_order.uid[2:])

    class Meta:
        model = WeldingProcessSpecification
        fields = '__all__'
        read_only_fields = ('id', 'work_order',)


class WeldingJointProcessAnalysisCreateSerializer(serializers.ModelSerializer):
    welding_seams = serializers.ListField(child=serializers.IntegerField(),
                                          write_only=True)

    def validate_welding_seams(self, welding_seam_ids):
        # 检查传入焊缝是否存在
        welding_seams = WeldingSeam.objects.filter(id__in=welding_seam_ids)
        if welding_seams.count() != len(welding_seam_ids):
            raise serializers.ValidationError("请检查传入焊缝ID")
        return welding_seams

    class Meta:
        model = WeldingJointProcessAnalysis
        fields = '__all__'


class WeldingJointProcessAnalysisSerializer(serializers.ModelSerializer):
    bm_1 = serializers.SerializerMethodField()
    bm_2 = serializers.SerializerMethodField()
    bm_thick_1 = serializers.SerializerMethodField()
    bm_thick_2 = serializers.SerializerMethodField()
    welding_work_instruction_index = serializers.SerializerMethodField(
        read_only=True)
    welding_work_instruction_id = serializers.SerializerMethodField(
        read_only=True)

    def get_welding_work_instruction_id(self, obj):
        return obj.weldingworkinstruction.id

    def get_welding_work_instruction_index(self, obj):
        return str(obj.weldingworkinstruction)

    def get_bm_1(self, obj):
        if obj.weldingseam_set.count() > 0:
            return obj.weldingseam_set.first().bm_1
        return None

    def get_bm_2(self, obj):
        if obj.weldingseam_set.count() > 0:
            return obj.weldingseam_set.first().bm_2
        return None

    def get_bm_thick_1(self, obj):
        if obj.weldingseam_set.count() > 0:
            return obj.weldingseam_set.first().bm_thick_1
        return None

    def get_bm_thick_2(self, obj):
        if obj.weldingseam_set.count() > 0:
            return obj.weldingseam_set.first().bm_thick_2
        return None

    class Meta:
        model = WeldingJointProcessAnalysis
        fields = '__all__'


class WeldingCertificationSerializer(serializers.ModelSerializer):
    weld_method_name = serializers.CharField(
        source='get_weld_method_display', read_only=True)

    class Meta:
        model = WeldingCertification
        fields = '__all__'


class WeldingWorkInstructionSerializer(serializers.ModelSerializer):
    bm_1 = serializers.SerializerMethodField()
    bm_2 = serializers.SerializerMethodField()
    bm_thick_1 = serializers.SerializerMethodField()
    bm_thick_2 = serializers.SerializerMethodField()
    wt_1 = serializers.SerializerMethodField()
    wt_2 = serializers.SerializerMethodField()
    work_order_uid = serializers.SerializerMethodField()
    uid = serializers.SerializerMethodField()
    weld_position = serializers.SerializerMethodField()
    welding_work_instruction_index = serializers.SerializerMethodField(
        read_only=True)

    def get_welding_work_instruction_index(self, obj):
        return str(obj)

    def get_weld_position(self, obj):
        return obj.detail.weldingseam_set.first().weld_position

    def get_uid(self, obj):
        return obj.detail.joint_index

    def get_work_order_uid(self, obj):
        return obj.detail.spec.work_order.uid

    def get_bm_1(self, obj):
        if obj.detail.weldingseam_set.count() > 0 > 0:
            return obj.detail.weldingseam_set.first().bm_1
        return None

    def get_bm_2(self, obj):
        if obj.detail.weldingseam_set.count() > 0 > 0:
            return obj.detail.weldingseam_set.first().bm_2
        return None

    def get_bm_thick_1(self, obj):
        if obj.detail.weldingseam_set.count() > 0 > 0:
            return obj.detail.weldingseam_set.first().bm_thick_1
        return None

    def get_bm_thick_2(self, obj):
        if obj.detail.weldingseam_set.count() > 0 > 0:
            return obj.detail.weldingseam_set.first().bm_thick_1
        return None

    def get_wt_1(self, obj):
        if obj.detail.weldingseam_set.count() > 0 > 0:
            return obj.detail.weldingseam_set.first().wt_1
        return None

    def get_wt_2(self, obj):
        if obj.detail.weldingseam_set.count() > 0 > 0:
            return obj.detail.weldingseam_set.first().wt_2
        return None

    class Meta:
        model = WeldingWorkInstruction
        fields = '__all__'


class AbstractQuotaItem4ProductionSerializer(serializers.ModelSerializer):
    work_order_id = serializers.IntegerField(
        source='process_material.lib.work_order.id')
    count = serializers.IntegerField(source='process_material.count',
                                     read_only=True)
    material = serializers.CharField(source='process_material.material.name',
                                     read_only=True)
    name = serializers.CharField(source='process_material.name')

    spec = serializers.CharField(source='process_material.spec')

    count = serializers.IntegerField(source='process_material.count')
    work_order_uid = serializers.CharField(
        source='process_material.lib.work_order.uid')

    class Meta:
        model = AbstractQuotaItem
        fields = ('id', 'work_order_uid', 'name', 'spec', 'material', 'count',
                  'work_order_id')


class CooperantItem4ProductionSerializer(
        AbstractQuotaItem4ProductionSerializer):

    class Meta(AbstractQuotaItem4ProductionSerializer.Meta):
        model = CooperantItem


class FirstFeedingItem4ProductionSerializer(
        AbstractQuotaItem4ProductionSerializer):

    class Meta(AbstractQuotaItem4ProductionSerializer.Meta):
        model = FirstFeedingItem


class BoughtInItem4ProductionSerializer(
        AbstractQuotaItem4ProductionSerializer):

    class Meta(AbstractQuotaItem4ProductionSerializer.Meta):
        model = BoughtInItem


class PrincipalQuotaItem4ProductionSerializer(serializers.ModelSerializer):
    work_order_id = serializers.CharField(
        source='quota_list.lib.work_order.id')
    work_order_uid = serializers.CharField(
        source='quota_list.lib.work_order.uid')
    material = serializers.CharField(source='material.name')

    class Meta:
        model = PrincipalQuotaItem
        fields = ('id', 'work_order_uid', 'size', 'material', 'count',
                  'work_order_id')


class WeldingQuotaItem4ProductionSerializer(serializers.ModelSerializer):
    work_order_id = serializers.CharField(
        source='quota_list.lib.work_order.id')
    work_order_uid = serializers.CharField(
        source='quota_list.lib.work_order.uid')
    material = serializers.CharField(source='material.name')

    class Meta:
        model = WeldingQuotaItem
        fields = ('id', 'work_order_uid', 'size', 'material', 'quota',
                  'work_order_id')


class AuxiliaryQuotaItem4ProductionSerializer(
        AbstractQuotaItem4ProductionSerializer):

    class Meta(AbstractQuotaItem4ProductionSerializer.Meta):
        model = AuxiliaryQuotaItem
