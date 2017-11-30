from rest_framework import viewsets, mixins

from Core.models import UserInfo, Department
from Core.serializers import UserInfoSerializer, DepartmentSerializer
from Core.utils.pagination import SmallResultsSetPagination


class UserInfoViewSet(mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    个人信息API
    """
    serializer_class = UserInfoSerializer
    pagination_class = SmallResultsSetPagination
    queryset = UserInfo.objects.all().order_by('pk')


class DepartmentViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    部门API
    """
    serializer_class = DepartmentSerializer
    pagination_class = SmallResultsSetPagination
    queryset = Department.objects.all().order_by('pk')
