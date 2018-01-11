from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import list_route
from rest_framework.response import Response

from Core import serializers, filters
from Core.models import Department
from Core.utils.pagination import SmallResultsSetPagination


class UserViewSet(viewsets.ModelViewSet):
    """
    用户信息API
    """
    pagination_class = SmallResultsSetPagination
    queryset = (User.objects.exclude(is_staff=True)
                .prefetch_related('info').order_by('pk'))
    filter_class = filters.UserFilter

    def destroy(self, request, pk=None):
        raise MethodNotAllowed(request.method)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCreateSerializer
        elif self.action == 'list':
            return serializers.UserListSerializer
        else:
            return serializers.UserSerializer

    @list_route()
    def non_production_users(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(info__isnull=False)
        queryset = queryset.filter(info__productionuser__isnull=True)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


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

    @list_route()
    def distribution(self, request):
        # TODO: Update to real departments
        # I strongly doubt this
        departments = Department.objects.all()[:4]
        mappings = {}
        for dep in departments:
            mappings[dep.group.name] = dep.id
        return Response(mappings)
