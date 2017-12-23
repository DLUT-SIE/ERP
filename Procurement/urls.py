from django.conf.urls import url, include

from rest_framework import routers
from Procurement.api import MaterialSubApplyViewSet
from Procurement.api import MaterialSubApplyItemViewSet
from Procurement.api import MaterialSubApplyCommentViewSet
from Procurement.api import MaterialExecutionViewSet
from Procurement.api import MaterialExecutionDetailViewSet

router = routers.SimpleRouter()
router.register(r'material_sub_applies', MaterialSubApplyViewSet)
router.register(r'material_sub_apply_items', MaterialSubApplyItemViewSet)
router.register(r'sub_spply_comments', MaterialSubApplyCommentViewSet)
router.register(r'material_executions', MaterialExecutionViewSet)
router.register(r'material_execution_details', MaterialExecutionDetailViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
]
