from django.contrib import admin

from Core.models import UserInfo, Department, WorkOrder, SubWorkOrder


admin.site.register(UserInfo)
admin.site.register(Department)
admin.site.register(WorkOrder)
admin.site.register(SubWorkOrder)
