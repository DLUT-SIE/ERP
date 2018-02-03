"""ERP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include

from Core.views.index import IndexView


urlpatterns = [
    url(r'^', include('Core.urls')),
    url(r'^', include('Distribution.urls')),
    url(r'^', include('Process.urls')),
    url(r'^', include('Procurement.urls')),
    url(r'^', include('Inventory.urls')),
    url(r'^', include('Production.urls')),
    url(r'^', IndexView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib import admin
    from rest_framework.documentation import include_docs_urls

    debug_urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^admin/', admin.site.urls),
        url(r'^api/', include_docs_urls(title='ERP APIs')),
    ]
    media_patterns = static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
    urlpatterns.extend(debug_urlpatterns)
    urlpatterns.extend(media_patterns)
