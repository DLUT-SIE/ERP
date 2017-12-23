from rest_framework import serializers

from Production.models import ProductionPlan


class ProductionPlanListSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='work_order.client',
                                   read_only=True)
    product = serializers.CharField(source='work_order.product',
                                    read_only=True)
    count = serializers.CharField(source='work_order.count',
                                  read_only=True)

    class Meta:
        model = ProductionPlan
        fields = ('work_order', 'status',
                  'plan_dt', 'client', 'product', 'count')


class ProductionPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionPlan
        fields = ('work_order', 'plan_dt')


class ProductionPlanUpdateSerializer(ProductionPlanListSerializer):
    class Meta(ProductionPlanListSerializer.Meta):
        read_only_fields = ('work_order', 'client', 'product', 'count')
