from django.conf.urls import url, include

from rest_framework import routers

from Process.api.process import ProcessLibraryViewSet
from Process.views import FileUploadView

router = routers.SimpleRouter()
router.register(r'process_libraries', ProcessLibraryViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/process_libraries/upload', FileUploadView.as_view())
]
