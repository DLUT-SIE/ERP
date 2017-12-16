from rest_framework import serializers

from Inventory.models import (
    WeldingMaterialEntry,)

from .entry_detail import WeldingMaterialEntryDetailSerializer


class WeldingMaterialEntrySerializer(serializers.ModelSerializer):
    pretty_status = serializers.CharField(source='get_status_display')
    purchaser = serializers.CharField(source='purchaser.username')
    inspector = serializers.CharField(source='inspector.username')
    keeper = serializers.CharField(source='keeper.username',
                                   allow_null=True, default=None)
    details = WeldingMaterialEntryDetailSerializer(many=True)

    class Meta:
        model = WeldingMaterialEntry
        fields = '__all__'


class WeldingMaterialEntryListSerializer(WeldingMaterialEntrySerializer):
    class Meta(WeldingMaterialEntrySerializer.Meta):
        fields = ('id', 'uid', 'create_dt', 'purchaser', 'inspector',
                  'status', 'pretty_status')
