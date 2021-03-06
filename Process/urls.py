from django.conf.urls import url, include

from rest_framework import routers

from Process.api import (
    ProcessLibraryViewSet, ProcessMaterialViewSet, CirculationRouteViewSet,
    ProcessRouteViewSet, TransferCardViewSet, TransferCardProcessViewSet,
    BoughtInItemViewSet, FirstFeedingItemViewSet, CooperantItemViewSet,
    PrincipalQuotaItemViewSet, QuotaListViewSet, WeldingQuotaItemViewSet,
    MaterialViewSet, AuxiliaryQuotaItemViewSet, WeldingSeamViewSet,
    TotalWeldingMaterialViewSet, WeldingMaterialViewSet, FluxMaterialViewSet,
    WeldingProcessSpecificationViewSet, WeldingJointProcessAnalysisViewSet,
    WeldingCertificationViewSet, WeldingWorkInstructionViewSet)
from Process.views import FileUploadView

router = routers.SimpleRouter()
router.register(r'process_libraries', ProcessLibraryViewSet)
router.register(r'process_materials', ProcessMaterialViewSet)
router.register(r'circulation_routes', CirculationRouteViewSet)
router.register(r'process_routes', ProcessRouteViewSet)
router.register(r'transfer_cards', TransferCardViewSet)
router.register(r'transfer_card_processes', TransferCardProcessViewSet)
router.register(r'bought_in_items', BoughtInItemViewSet)
router.register(r'first_feeding_items', FirstFeedingItemViewSet)
router.register(r'cooperant_items', CooperantItemViewSet)
router.register(r'principal_quota_items', PrincipalQuotaItemViewSet)
router.register(r'quota_lists', QuotaListViewSet)
router.register(r'welding_quota_items', WeldingQuotaItemViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'auxiliary_quota_items', AuxiliaryQuotaItemViewSet)
router.register(r'welding_seams', WeldingSeamViewSet)
router.register(r'total_welding_materials', TotalWeldingMaterialViewSet)
router.register(r'welding_materials', WeldingMaterialViewSet)
router.register(r'flux_materials', FluxMaterialViewSet)
router.register(r'welding_process_specifications',
                WeldingProcessSpecificationViewSet)
router.register(r'welding_joint_process_analyses',
                WeldingJointProcessAnalysisViewSet)
router.register(r'welding_certifications', WeldingCertificationViewSet)
router.register(r'welding_work_instructions', WeldingWorkInstructionViewSet)

urlpatterns = [
    url(r'^api/process_libraries/upload/', FileUploadView.as_view()),
    url(r'^api/', include(router.urls)),
]
