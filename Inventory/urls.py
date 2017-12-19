from django.conf.urls import url, include

from rest_framework import routers

from Inventory import api


router = routers.SimpleRouter()
router.register(r'welding_material_entry_details',
                api.WeldingMaterialEntryDetailViewSet)
router.register(r'steel_material_entry_details',
                api.SteelMaterialEntryDetailViewSet)
router.register(r'auxiliary_material_entry_details',
                api.AuxiliaryMaterialEntryDetailViewSet)
router.register(r'bought_in_component_entry_details',
                api.BoughtInComponentEntryDetailViewSet)

router.register(r'welding_material_entries',
                api.WeldingMaterialEntryViewSet)
router.register(r'steel_material_entries',
                api.SteelMaterialEntryViewSet)
router.register(r'auxiliary_material_entries',
                api.AuxiliaryMaterialEntryViewSet)
router.register(r'bought_in_component_entries',
                api.BoughtInComponentEntryViewSet)

router.register(r'welding_material_inventory_details',
                api.WeldingMaterialInventoryDetailViewSet)
router.register(r'steel_material_inventory_details',
                api.SteelMaterialInventoryDetailViewSet)
router.register(r'auxiliary_material_inventory_details',
                api.AuxiliaryMaterialInventoryDetailViewSet)
router.register(r'bought_in_component_inventory_details',
                api.BoughtInComponentInventoryDetailViewSet)

router.register(r'steel_material_apply_details',
                api.SteelMaterialApplyDetailViewSet)
router.register(r'bought_in_component_apply_details',
                api.BoughtInComponentApplyDetailViewSet)

router.register(r'welding_material_apply_cards',
                api.WeldingMaterialApplyCardViewSet)
router.register(r'steel_material_apply_cards',
                api.SteelMaterialApplyCardViewSet)
router.register(r'auxiliary_material_apply_cards',
                api.AuxiliaryMaterialApplyCardViewSet)
router.register(r'bought_in_component_apply_cards',
                api.BoughtInComponentApplyCardViewSet)

router.register(r'board_steel_material_refund_details',
                api.BoardSteelMaterialRefundDetailViewSet)
router.register(r'bar_steel_material_refund_details',
                api.BarSteelMaterialRefundDetailViewSet)

router.register(r'welding_material_refund_cards',
                api.WeldingMaterialRefundCardViewSet)
router.register(r'steel_material_refund_cards',
                api.SteelMaterialRefundCardViewSet)
router.register(r'bought_in_component_refund_cards',
                api.BoughtInComponentRefundCardViewSet)

router.register(r'warehouses',
                api.WarehouseViewSet)
router.register(r'welding_material_humiture_records',
                api.WeldingMaterialHumitureRecordViewSet)
router.register(r'welding_material_bake_records',
                api.WeldingMaterialBakeRecordViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
