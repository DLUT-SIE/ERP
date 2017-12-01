from django.conf.urls import url, include

from rest_framework import routers

from Distribution.api import ProductViewSet, BiddingDocumentViewSet

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'bidding_documents', BiddingDocumentViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
