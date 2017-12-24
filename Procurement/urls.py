from django.conf.urls import url, include

from rest_framework import routers
from Procurement import api

router = routers.SimpleRouter()
router.register(r'material_sub_applies', api.MaterialSubApplyViewSet)
router.register(r'material_sub_apply_items', api.MaterialSubApplyItemViewSet)
router.register(r'sub_spply_comments', api.MaterialSubApplyCommentViewSet)
router.register(r'material_executions', api.MaterialExecutionViewSet)
router.register(r'material_execution_details',
                api.MaterialExecutionDetailViewSet)
router.register(r'status_changes', api.StatusChangeViewSet)
router.register(r'suppliers', api.SupplierViewSet)
router.register(r'supplier_documents', api.SupplierDocumentViewSet)
router.register(r'supplier_quotations', api.QuotationViewSet)
router.register(r'contact_details', api.ContractDetailViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
