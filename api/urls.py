"""
Core URL routing
"""
from django.contrib import admin
from django.urls import path, include


handler400 = "apps.core.views.handler404"
handler403 = "apps.core.views.handler404"
handler404 = "apps.core.views.handler404"
handler500 = "apps.core.views.handler500"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
]
