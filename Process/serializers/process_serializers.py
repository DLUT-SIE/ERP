from rest_framework import serializers

from Process.models import ProcessLibrary


class ProcessLibrarySerializer(serializers.ModelSerializer):
    process_materials = serializers.PrimaryKeyRelatedField(many=True,
                                                           read_only=True)

    class Meta:
        model = ProcessLibrary
        fields = '__all__'


class ProcessLibraryListSerializer(ProcessLibrarySerializer):
    name = serializers.CharField(source='work_order.product')
    status = serializers.SerializerMethodField()

    class Meta(ProcessLibrarySerializer.Meta):
        fields = ('id', 'name', 'status',
                  'proofreader', 'writer')

    def get_status(self, obj):
        if obj.process_materials.count() == 0:
            return 0
        elif obj.writer is not None:
            return 2
        return 1


class ProcessLibraryCreateSerializer(ProcessLibrarySerializer):
    file = serializers.FileField(allow_empty_file=False)

    class Meta(ProcessLibrarySerializer.Meta):
        fields = '__all__'
