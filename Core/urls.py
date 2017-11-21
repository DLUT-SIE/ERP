from django.conf.urls import url

from Core.views import LoginView, LogoutView, home


urlpatterns = [
    url(r'^$', home.HomeView.as_view(), name='home'),
    url(r'^login/', LoginView.as_view(template_name='login.html')),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
]
