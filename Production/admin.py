from django.contrib import admin

from Production.models import (
    SubMaterial, ProductionWorkGroup, ProductionUser,
    ProcessDetail, ComprehensiveDepartmentFileList,
    ProductionPlan)


admin.site.register(SubMaterial)
admin.site.register(ProductionWorkGroup)
admin.site.register(ProductionUser)
admin.site.register(ProcessDetail)
admin.site.register(ComprehensiveDepartmentFileList)
admin.site.register(ProductionPlan)
