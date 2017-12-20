from django.conf.urls import url, include

from rest_framework import routers

from Process.api import (
    ProcessLibraryViewSet, ProcessMaterialViewSet, CirculationRouteViewSet,
    ProcessRouteViewSet)
from Process.views import FileUploadView

router = routers.SimpleRouter()
router.register(r'process_libraries', ProcessLibraryViewSet)
router.register(r'process_materials', ProcessMaterialViewSet)
router.register(r'circulation_routes', CirculationRouteViewSet)
router.register(r'process_routes', ProcessRouteViewSet)
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^process_libraries/upload', FileUploadView.as_view())
]
