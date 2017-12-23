from django.conf.urls import url, include

from rest_framework import routers

from Production.api import ProcessDetailViewSet, SubMaterialViewSet

router = routers.SimpleRouter()
router.register(r'process_details', ProcessDetailViewSet)
router.register(r'sub_materials', SubMaterialViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
