from django.db import transaction
from django.contrib.auth.models import User, Group

from rest_framework import serializers

from Core.models import UserInfo, Department


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('phone', 'mobile', 'gender')


class UserSerializer(serializers.ModelSerializer):
    info = UserInfoSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'info')


class UserListSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('id', 'first_name', 'email')


class UserCreateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('username', 'password', 'email', 'first_name',
                  'last_name', 'info')

    def create(self, validated_data):
        with transaction.atomic():
            info_dict = validated_data.pop('info')
            user = super().create(validated_data)
            UserInfo.objects.create(user=user, **info_dict)
            return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class DepartmentSerializer(serializers.ModelSerializer):
    group = GroupSerializer(help_text='组名')

    class Meta:
        model = Department
        fields = ('id', 'group', 'superior', 'admin', 'short_name')

    def create(self, validated_data):
        with transaction.atomic():
            group_dict = validated_data.pop('group')
            group = Group.objects.create(**group_dict)
            dep = Department.objects.create(group=group, **validated_data)
        return dep


class DepartmentListSerializer(DepartmentSerializer):
    class Meta(DepartmentSerializer.Meta):
        fields = ('id', 'superior', 'admin', 'short_name')
