from django.conf.urls import url, include

from rest_framework import routers

from Core.views import LoginView, LogoutView, home
from Core.api import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^$', home.HomeView.as_view(), name='home'),
    url(r'^login/', LoginView.as_view(template_name='login.html')),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^api/', include(router.urls)),
]
