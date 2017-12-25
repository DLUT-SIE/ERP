from django.conf.urls import url, include

from rest_framework import routers

from Production.api import ProductionPlanViewSet
from Production.api import ProcessDetailViewSet, SubMaterialViewSet
from Production.api import SubMaterialLedgersViewSet

router = routers.SimpleRouter()
router.register(r'production_plans', ProductionPlanViewSet)
router.register(r'process_details', ProcessDetailViewSet)
router.register(r'sub_materials', SubMaterialViewSet)
router.register(r'sub_material_ledgers', SubMaterialLedgersViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
