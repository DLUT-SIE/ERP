from django.conf.urls import url, include

from rest_framework import routers

from Distribution.api import ProductViewSet, BiddingDocumentViewSet

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)
router.register(r'biddingdocument', BiddingDocumentViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
