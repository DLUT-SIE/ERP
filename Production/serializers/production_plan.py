from rest_framework import serializers

from Production.models import ProductionPlan


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
    class Meta:
        model = ProductionPlan
        fields = ('work_order', 'plan_dt', 'remark')


class ProductionPlanUpdateSerializer(ProductionPlanListSerializer):
    class Meta(ProductionPlanListSerializer.Meta):
        read_only_fields = ('work_order', 'client', 'product', 'count')
