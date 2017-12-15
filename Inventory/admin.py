from django.contrib import admin

from Inventory.models import (
    WeldingMaterialEntry, SteelMaterialEntry, AuxiliaryMaterialEntry,
    BoughtInComponentEntry, WeldingMaterialEntryDetail,
    SteelMaterialEntryDetail, AuxiliaryMaterialEntryDetail,
    BoughtInComponentEntryDetail, WeldingMaterialInventoryDetail,
    SteelMaterialInventoryDetail, AuxiliaryMaterialInventoryDetail,
    BoughtInComponentInventoryDetail, WeldingMaterialApplyCard,
    SteelMaterialApplyCard, AuxiliaryMaterialApplyCard,
    BoughtInComponentApplyCard,
    SteelMaterialApplyDetail, AuxiliaryMaterialApplyDetail,
    BoughtInComponentApplyDetail, SteelMaterialRefundCard,
    WeldingMaterialRefundCard, BoughtInComponentRefundCard,
    BarSteelMaterialRefundDetail,
    BoardSteelMaterialRefundDetail, BoughtInComponentRefundDetail,
    Warehouse, WeldingMaterialHumitureRecord, WeldingMaterialBakeRecord,
    WeldingWarehouseThreshold, InventoryTerminationRecord)


admin.site.register(WeldingMaterialEntry)
admin.site.register(SteelMaterialEntry)
admin.site.register(AuxiliaryMaterialEntry)
admin.site.register(BoughtInComponentEntry)
admin.site.register(WeldingMaterialEntryDetail)
admin.site.register(SteelMaterialEntryDetail)
admin.site.register(AuxiliaryMaterialEntryDetail)
admin.site.register(BoughtInComponentEntryDetail)
admin.site.register(WeldingMaterialInventoryDetail)
admin.site.register(SteelMaterialInventoryDetail)
admin.site.register(AuxiliaryMaterialInventoryDetail)
admin.site.register(BoughtInComponentInventoryDetail)
admin.site.register(WeldingMaterialApplyCard)
admin.site.register(SteelMaterialApplyCard)
admin.site.register(AuxiliaryMaterialApplyCard)
admin.site.register(BoughtInComponentApplyCard)
admin.site.register(SteelMaterialApplyDetail)
admin.site.register(AuxiliaryMaterialApplyDetail)
admin.site.register(BoughtInComponentApplyDetail)
admin.site.register(SteelMaterialRefundCard)
admin.site.register(WeldingMaterialRefundCard)
admin.site.register(BoughtInComponentRefundCard)
admin.site.register(BarSteelMaterialRefundDetail)
admin.site.register(BoardSteelMaterialRefundDetail)
admin.site.register(BoughtInComponentRefundDetail)
admin.site.register(Warehouse)
admin.site.register(WeldingMaterialHumitureRecord)
admin.site.register(WeldingMaterialBakeRecord)
admin.site.register(WeldingWarehouseThreshold)
admin.site.register(InventoryTerminationRecord)
