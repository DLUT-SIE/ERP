from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied

from Distribution.models import Product
from Distribution.serializers import (ProductSerializer,
                                      BiddingDocumentSerializer)


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    产品信息API
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request):
        """
        返回产品信息列表

        GET /api/products/?page=&limit=

        =================== =========== ============================
        参数                参数类型    描述
        ------------------- ----------- ----------------------------
        page(Required)      int         产品信息列表的指定页数
        ------------------- ----------- ----------------------------
        limit(Required)     int         每页最大产品信息数量
        =================== =========== ============================


        =================== =========== ============================
        返回字段            返回类型    描述
        ------------------- ----------- ----------------------------
        name                str         产品名称
        ------------------- ----------- ----------------------------
        approved            bool        产品审核结果
        ------------------- ----------- ----------------------------
        terminated          bool        终止状态
        =================== =========== ============================
        """
        return super().list(request)

    def create(self, request):
        raise PermissionDenied()
        return super().create(request)

    def retrieve(self, request, pk=None):
        """
        返回指定ID的产品信息

        GET /api/products/id/

        =================== =========== ============================
        参数                参数类型    描述
        ------------------- ----------- ----------------------------
        id(Required)        int         指定产品的ID
        =================== =========== ============================

        =================== =========== ============================
        返回字段            返回类型    描述
        ------------------- ----------- ----------------------------
        name                str         产品名称
        ------------------- ----------- ----------------------------
        approved            bool        产品审核结果
        ------------------- ----------- ----------------------------
        terminated          bool        终止状态
        =================== =========== ============================
        """
        return super().retrieve(request, pk)
