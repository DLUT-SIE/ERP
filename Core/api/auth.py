from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from Core import serializers
from Core.models import Department
from Core.utils.pagination import SmallResultsSetPagination


class UserViewSet(viewsets.ModelViewSet):
    """
    用户信息API
    """
    pagination_class = SmallResultsSetPagination
    queryset = User.objects.exclude(is_staff=True).order_by('pk')

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCreateSerializer
        elif self.action == 'list':
            return serializers.UserListSerializer
        else:
            return serializers.UserSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    部门API
    """
    pagination_class = SmallResultsSetPagination
    queryset = Department.objects.all().order_by('pk')

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.DepartmentListSerializer
        else:
            return serializers.DepartmentSerializer
