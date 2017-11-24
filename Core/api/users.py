from django.contrib.auth.models import User

from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied

from Core.serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    用户帐户信息API
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        """
        返回用户信息列表

        GET /api/users/?page=&limit=

        =================== =========== ============================
        参数                参数类型    描述
        ------------------- ----------- ----------------------------
        page(Required)      int         用户信息列表的指定页数
        ------------------- ----------- ----------------------------
        limit(Required)     int         每页最大用户信息数量
        =================== =========== ============================


        =================== =========== ============================
        返回字段            返回类型    描述
        ------------------- ----------- ----------------------------
        url                 str         该用户详细信息请求链接
        ------------------- ----------- ----------------------------
        username            str
        ------------------- ----------- ----------------------------
        email               str
        ------------------- ----------- ----------------------------
        is_staff            bool        是否为工作人员
        =================== =========== ============================
        """
        return super().list(request)

    def create(self, request):
        raise PermissionDenied()
        return super().create(request)

    def retrieve(self, request, pk=None):
        """
        返回指定ID的用户信息

        GET /api/users/id/

        =================== =========== ============================
        参数                参数类型    描述
        ------------------- ----------- ----------------------------
        id(Required)        int         指定用户的ID
        =================== =========== ============================


        =================== =========== ============================
        返回字段            返回类型    描述
        ------------------- ----------- ----------------------------
        url                 str         该用户详细信息请求链接
        ------------------- ----------- ----------------------------
        username            str
        ------------------- ----------- ----------------------------
        email               str
        ------------------- ----------- ----------------------------
        is_staff            bool        是否为工作人员
        =================== =========== ============================
        """
        return super().retrieve(request, pk)
