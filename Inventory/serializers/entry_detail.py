from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialEntryDetail,)


class WeldingMaterialEntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldingMaterialEntryDetail
        fields = '__all__'
