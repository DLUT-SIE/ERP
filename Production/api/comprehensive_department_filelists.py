from rest_framework import viewsets

from Core.utils.pagination import SmallResultsSetPagination
from Production import serializers
from Production.filters import ComprehensiveDepartmentFileListFilter
from Production.models import ComprehensiveDepartmentFileList


class ComprehensiveDepartmentFileListViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    queryset = ComprehensiveDepartmentFileList.objects.all().order_by('-pk')
    filter_class = ComprehensiveDepartmentFileListFilter
    serializer_class = serializers.ComprehensiveDepartmentFileListSerializer
