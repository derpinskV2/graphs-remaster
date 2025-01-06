from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.conf import settings

from config.api import v1

urlpatterns = [
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/", v1.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
