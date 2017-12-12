from django.conf.urls import url, include

from rest_framework import routers
from Procurement.api import MaterialSubApplyViewSet
from Procurement.api import MaterialSubApplyItemsViewSet

router = routers.SimpleRouter()
router.register(r'material_subapplys', MaterialSubApplyViewSet)
router.register(r'material_subapply_items', MaterialSubApplyItemsViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
