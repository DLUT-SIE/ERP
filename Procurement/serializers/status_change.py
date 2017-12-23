from rest_framework import serializers

from Procurement.models import StatusChange


class StatusChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatusChange
        fields = '__all__'
        read_only_fields = ('normal_change', 'change_user')
