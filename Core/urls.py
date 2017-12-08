from django.conf.urls import url, include

from rest_framework import routers

from Core.views import LoginView, LogoutView
from Core.api import (UserInfoViewSet, DepartmentViewSet,
                      WorkOrderViewSet, SubWorkOrderViewSet)

router = routers.SimpleRouter()
router.register(r'userinfo', UserInfoViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'workorder', WorkOrderViewSet)
router.register(r'subworkorder', SubWorkOrderViewSet)

urlpatterns = [
    url(r'^login/', LoginView.as_view(template_name='login.html')),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^api/', include(router.urls)),
]
