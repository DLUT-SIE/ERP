from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction

from Core.utils.pagination import SmallResultsSetPagination
from Process.models import ProcessMaterial

from Production import serializers
from Production.models import ProcessDetail, SubMaterial
from Production.filters import ProcessDetailFilter


class ProcessDetailViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ProcessDetail.objects.all().order_by('-pk')
    filter_class = ProcessDetailFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ProcessDetailCreateSerializer
        elif self.action == 'list':
            return serializers.ProcessDetailListSerializer
        elif self.action in ('partial_update', 'update'):
            return serializers.ProcessDetailSimpleSerializer
        else:
            return serializers.ProcessDetailSerializer


class SubMaterialViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = SubMaterial.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.SubMaterialCreateSerializer
        else:
            return serializers.SubMaterialSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('sub_order', None) is not None:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        elif request.data.get('material', None) is not None:
            process_data = []
            process_material = ProcessMaterial.objects.filter(
                id=request.data['material'])
            if process_material.count() != 1:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            work_order = process_material[0].lib.work_order
            sub_orders = work_order.subworkorder_set.all()
            with transaction.atomic():
                for sub_order in sub_orders:
                    request.data['sub_order'] = sub_order.id
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    process_data.append(serializer.data)
            headers = self.get_success_headers(process_data)
            return Response(process_data, status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
