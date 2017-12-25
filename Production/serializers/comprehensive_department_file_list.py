from rest_framework import serializers

from Production.models import ComprehensiveDepartmentFileList


class ComprehensiveDepartmentFileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComprehensiveDepartmentFileList
        fields = ('sub_order', 'sketch', 'pressure_test',
                  'process_lib', 'product_graph', 'encasement_graph',
                  'shipping_mark', 'encasement_list', 'coating_detail')
