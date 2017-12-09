from django.conf.urls import url, include

from rest_framework import routers

from Core.views import LoginView, LogoutView
from Core.api import (UserViewSet, DepartmentViewSet,
                      WorkOrderViewSet, SubWorkOrderViewSet)

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'work_orders', WorkOrderViewSet)
router.register(r'sub_work_orders', SubWorkOrderViewSet)

urlpatterns = [
    url(r'^login/', LoginView.as_view(template_name='login.html')),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^api/', include(router.urls)),
]
