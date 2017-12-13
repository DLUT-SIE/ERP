from django.contrib import admin

from Procurement.models import (
    PurchaseOrder, ProcurementMaterial, BiddingSheet, BiddingApplication,
    ParityRatioCard, BiddingAcceptance, BiddingComment, SubApplyComment,
    ContractDetail, MaterialExecution, MaterialExecutionDetail,
    ArrivalInspection, ProcessFollowingInfo, StatusChange, Quotation,
    MaterialSubApply, MaterialSubApplyItems, Supplier, SupplierCheck,
    SupplierDocument, SupplyRelationship)


admin.site.register(PurchaseOrder)
admin.site.register(ProcurementMaterial)
admin.site.register(BiddingSheet)
admin.site.register(BiddingApplication)
admin.site.register(ParityRatioCard)
admin.site.register(BiddingAcceptance)
admin.site.register(BiddingComment)
admin.site.register(SubApplyComment)
admin.site.register(ContractDetail)
admin.site.register(MaterialExecution)
admin.site.register(MaterialExecutionDetail)
admin.site.register(ArrivalInspection)
admin.site.register(ProcessFollowingInfo)
admin.site.register(StatusChange)
admin.site.register(Quotation)
admin.site.register(MaterialSubApply)
admin.site.register(MaterialSubApplyItems)
admin.site.register(Supplier)
admin.site.register(SupplierCheck)
admin.site.register(SupplierDocument)
admin.site.register(SupplyRelationship)
