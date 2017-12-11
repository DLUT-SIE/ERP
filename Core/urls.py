from django.conf.urls import url, include

from rest_framework import routers

from Core.api import (UserViewSet, DepartmentViewSet,
                      WorkOrderViewSet, SubWorkOrderViewSet)
from Core.views.base import LoginView

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'work_orders', WorkOrderViewSet)
router.register(r'sub_work_orders', SubWorkOrderViewSet)

urlpatterns = [
    url(r'^login/', LoginView.as_view()),
    url(r'^api/', include(router.urls)),
]
