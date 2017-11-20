#!/usr/bin/env python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-11-20 16:00
# Last modified: 2017-11-20 16:00
# Filename: urls.py
# Description:
from django.conf.urls import url

from Core.views import LoginView, LogoutView, home


urlpatterns = [
    url(r'^$', home.HomeView.as_view(), name='home'),
    url(r'^login/', LoginView.as_view(template_name='login.html')),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
]
