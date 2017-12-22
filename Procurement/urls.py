from django.conf.urls import url, include

from rest_framework import routers
from Procurement.api import MaterialSubApplyViewSet
from Procurement.api import MaterialSubApplyItemsViewSet
from Procurement.api import MaterialSubApplyCommentsViewSet

router = routers.SimpleRouter()
router.register(r'material_sub_applies', MaterialSubApplyViewSet)
router.register(r'material_sub_apply_items', MaterialSubApplyItemsViewSet)
router.register(r'sub_spply_comments', MaterialSubApplyCommentsViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
