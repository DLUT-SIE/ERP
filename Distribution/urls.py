from django.conf.urls import url, include

from rest_framework import routers

from Distribution.api import ProductViewSet

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
