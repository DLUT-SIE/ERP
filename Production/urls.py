from django.conf.urls import url, include

from rest_framework import routers


from Production.api import (ProductionPlanViewSet,
                            ProcessDetailViewSet,
                            SubMaterialViewSet,
                            ProductionWorkGroupViewSet,
                            ProductionUserViewSet,
                            SubMaterialLedgersViewSet,
                            ComprehensiveDepartmentFileListViewSet,
                            ManHourMessageViewSet)

router = routers.SimpleRouter()
router.register(r'production_plans', ProductionPlanViewSet)
router.register(r'process_details', ProcessDetailViewSet)
router.register(r'sub_materials', SubMaterialViewSet)
router.register(r'production_work_groups', ProductionWorkGroupViewSet)
router.register(r'production_users', ProductionUserViewSet)
router.register(r'sub_material_ledgers', SubMaterialLedgersViewSet)
router.register(r'comprehensive_department_file_lists',
                ComprehensiveDepartmentFileListViewSet)
router.register(r'man_hour_messages', ManHourMessageViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
