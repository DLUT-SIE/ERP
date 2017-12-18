from django.conf.urls import url, include

from rest_framework import routers

from Process.api import ProcessLibraryViewSet, ProcessMaterialViewSet
from Process.views import FileUploadView

router = routers.SimpleRouter()
router.register(r'process_libraries', ProcessLibraryViewSet)
router.register(r'process_materials', ProcessMaterialViewSet)
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/process_libraries/upload', FileUploadView.as_view())
]
