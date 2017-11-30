from rest_framework import serializers

from Core.models import UserInfo, Department


class UserInfoSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name',
                                       read_only=True)
    last_name = serializers.CharField(source='user.last_name',
                                      read_only=True)

    class Meta:
        model = UserInfo
        fields = ('id', 'first_name', 'last_name',
                  'email', 'phone', 'mobile', 'gender')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'superior', 'admin', 'short_name')
