from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from .api import v1
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", v1.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
