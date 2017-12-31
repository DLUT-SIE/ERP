from rest_framework import serializers

from Core.serializers import UserSerializer
from Production.models import ProductionUser, ProductionWorkGroup


class ProductionWorkGroupSerializer(serializers.ModelSerializer):
    process_name = serializers.CharField(source='get_process_display',
                                         read_only=True)

    class Meta:
        model = ProductionWorkGroup
        fields = ('id', 'name', 'process', 'process_name')


class ProductionUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_info.user', read_only=True)
    work_group_name = serializers.CharField(source='work_group.name',
                                            allow_null=True, read_only=True)

    class Meta:
        model = ProductionUser
        fields = ('id', 'user_info', 'work_group', 'work_group_name', 'user')


class ProductionUserUpdateSerializer(ProductionUserSerializer):
    class Meta(ProductionUserSerializer.Meta):
        read_only_fields = ('user_info',)
