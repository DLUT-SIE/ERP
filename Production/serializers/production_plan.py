from rest_framework import serializers

from Production.models import ProductionPlan
from Core.models import WorkOrder


class ProductionPlanListSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='work_order.client',
                                   read_only=True)
    product = serializers.CharField(source='work_order.product',
                                    read_only=True)
    count = serializers.CharField(source='work_order.count',
                                  read_only=True)
    status_description = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductionPlan
        fields = ('id', 'work_order', 'status', 'status_description',
                  'plan_dt', 'client', 'product', 'count', 'remark')

    def get_status_description(self, obj):
        if obj.status == 1:
            return '在制'
        elif obj.status == 0:
            return '必保'
        else:
            return ''


class ProductionPlanCreateSerializer(serializers.ModelSerializer):
    work_order_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = ProductionPlan
        fields = ('work_order_ids',)

    def validate_work_order_ids(self, value):
        queryset = WorkOrder.objects.filter(id__in=value)
        if len(queryset) == len(value):
            return queryset
        else:
            raise serializers.ValidationError("id does not exist!")

    def create(self, validated_data):
        querysetlist = []
        for instance in validated_data['work_order_ids']:
            querysetlist.append(ProductionPlan(work_order=instance))
        return self.Meta.model.objects.bulk_create(querysetlist)


class ProductionPlanUpdateSerializer(ProductionPlanListSerializer):
    class Meta(ProductionPlanListSerializer.Meta):
        read_only_fields = ('work_order', 'client', 'product', 'count')
