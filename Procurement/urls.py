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
router.register(r'purchase_orders', api.PurchaseOrderViewSet)
router.register(r'procurement_materials', api.ProcurementMaterialViewSet)
router.register(r'bidding_sheets', api.BiddingSheetViewSet)
router.register(r'bidding_applications', api.BiddingApplicationViewSet)
router.register(r'supply_relationships', api.SupplyRelationshipViewSet)
router.register(r'bidding_acceptances', api.BiddingAcceptanceViewSet)
router.register(r'supplier_checks', api.SupplierCheckViewSet)
router.register(r'process_following_infos', api.ProcessFollowingInfoViewSet)
router.register(r'arrival_inspections', api.ArrivalInspectionViewSet)
router.register(r'parity_ratio_cards', api.ParityRatioCardViewSet)
router.register(r'bidding_comments', api.BiddingCommentViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
