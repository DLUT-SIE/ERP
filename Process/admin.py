from django.contrib import admin

from Process.models import (
    Material, ProcessLibrary, ProcessMaterial,
    ProcessRoute, CirculationRoute, TransferCard, TransferCardProcess,
    ProcessReview, ProgrammingBlankingChart, QuotaList, AuxiliaryQuotaItem,
    CooperantItem, FirstFeedingItem, BoughtInItem, PrincipalQuotaItem,
    WeldingQuotaItem, WeldingProcessSpecification, WeldingCertification,
    WeldingJointProcessAnalysis, WeldingSeam, WeldingWorkInstruction,
    WeldingWorkInstructionProcess, WeldingWorkInstructionExamination,
    WeldingLayerCard)


admin.site.register(Material)
admin.site.register(ProcessLibrary)
admin.site.register(ProcessMaterial)
admin.site.register(ProcessRoute)
admin.site.register(CirculationRoute)
admin.site.register(TransferCard)
admin.site.register(TransferCardProcess)
admin.site.register(ProcessReview)
admin.site.register(ProgrammingBlankingChart)
admin.site.register(QuotaList)
admin.site.register(AuxiliaryQuotaItem)
admin.site.register(CooperantItem)
admin.site.register(FirstFeedingItem)
admin.site.register(BoughtInItem)
admin.site.register(PrincipalQuotaItem)
admin.site.register(WeldingQuotaItem)
admin.site.register(WeldingProcessSpecification)
admin.site.register(WeldingCertification)
admin.site.register(WeldingJointProcessAnalysis)
admin.site.register(WeldingSeam)
admin.site.register(WeldingWorkInstruction)
admin.site.register(WeldingWorkInstructionProcess)
admin.site.register(WeldingWorkInstructionExamination)
admin.site.register(WeldingLayerCard)
